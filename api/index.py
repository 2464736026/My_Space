from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
import traceback
from typing import Optional, Dict, Any

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

# 延迟导入，避免在模块加载时就失败
pdf_parser = None
cache_manager = None
PDFParser = None
AIService = None
CacheManager = None

def lazy_import():
    """延迟导入依赖模块"""
    global pdf_parser, cache_manager, PDFParser, AIService, CacheManager
    
    if PDFParser is None:
        try:
            from services.pdf_parser import PDFParser as _PDFParser
            from services.ai_service import AIService as _AIService
            from utils.cache import CacheManager as _CacheManager
            
            PDFParser = _PDFParser
            AIService = _AIService
            CacheManager = _CacheManager
            
            pdf_parser = PDFParser()
            cache_manager = CacheManager()
            
            print("Successfully imported all services")
        except ImportError as e:
            print(f"Import error: {e}")
            print(f"Current directory: {os.getcwd()}")
            print(f"Directory contents: {os.listdir('.')}")
            raise

app = FastAPI(title="AI Resume Analyzer", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局AI服务实例
ai_service = None

def get_ai_service():
    """获取AI服务实例"""
    global ai_service
    if ai_service is None:
        try:
            lazy_import()  # 确保已导入
            ai_service = AIService()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
    return ai_service

class JobRequirement(BaseModel):
    job_title: str
    job_description: str
    required_skills: str = ""
    experience_level: str = ""

class ResumeAnalysisResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str = ""

@app.get("/")
async def root():
    """健康检查端点"""
    return {
        "message": "AI Resume Analyzer API", 
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/api/upload-resume",
            "/api/match-job"
        ]
    }

@app.get("/api/health")
async def health_check():
    """详细健康检查"""
    try:
        # 检查环境变量
        api_key = os.getenv("OPENAI_API_KEY", "")
        
        return {
            "status": "healthy",
            "openai_configured": bool(api_key and len(api_key) > 20),
            "openai_model": os.getenv("OPENAI_MODEL", "not set"),
            "openai_base_url": os.getenv("OPENAI_BASE_URL", "not set")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """上传并解析简历"""
    try:
        lazy_import()  # 确保已导入
        
        print(f"Received file: {file.filename}")
        
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="只支持PDF格式文件")
        
        content = await file.read()
        print(f"File size: {len(content)} bytes")
        
        text_content = pdf_parser.extract_text(content)
        print(f"Extracted text length: {len(text_content)}")
        
        if not text_content or len(text_content) < 50:
            raise HTTPException(status_code=400, detail="PDF文件内容为空或无法解析")
        
        ai = get_ai_service()
        print("AI service initialized")
        
        extracted_info = ai.extract_resume_info(text_content)
        print(f"Extracted info: {extracted_info}")
        
        resume_id = cache_manager.cache_resume(extracted_info, text_content)
        print(f"Resume cached with ID: {resume_id}")
        
        return {
            "success": True,
            "data": {
                "resume_id": resume_id,
                "extracted_info": extracted_info,
                "text_preview": text_content[:500] + "..." if len(text_content) > 500 else text_content
            },
            "message": "简历解析成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in upload_resume: {str(e)}")
        print(traceback.format_exc())
        return {"success": False, "message": f"简历解析失败: {str(e)}"}

@app.post("/api/match-job")
async def match_job(request_data: dict):
    """简历与岗位匹配评分"""
    try:
        lazy_import()  # 确保已导入
        
        resume_id = request_data.get("resume_id")
        if not resume_id:
            raise HTTPException(status_code=400, detail="缺少resume_id参数")
        
        job_req = JobRequirement(
            job_title=request_data.get("job_title", ""),
            job_description=request_data.get("job_description", ""),
            required_skills=request_data.get("required_skills", ""),
            experience_level=request_data.get("experience_level", "")
        )
        
        resume_data = cache_manager.get_resume(resume_id)
        if not resume_data:
            raise HTTPException(status_code=404, detail="简历数据未找到")
        
        ai = get_ai_service()
        match_result = ai.analyze_job_match(resume_data["extracted_info"], job_req.dict())
        
        return {"success": True, "data": match_result, "message": "匹配评分完成"}
    except HTTPException:
        raise
    except Exception as e:
        return {"success": False, "message": f"匹配评分失败: {str(e)}"}


# Vercel Serverless Function Handler
from mangum import Mangum
handler = Mangum(app, lifespan="off")
