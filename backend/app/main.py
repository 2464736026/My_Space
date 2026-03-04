from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional, Dict, Any
import json

from .services.pdf_parser import PDFParser
from .services.ai_service import AIService
from .utils.cache import CacheManager

app = FastAPI(title="AI Resume Analyzer", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
pdf_parser = PDFParser()
cache_manager = CacheManager()

# 初始化AI服务（延迟初始化，避免启动时就检查API密钥）
ai_service = None

def get_ai_service():
    """获取AI服务实例"""
    global ai_service
    if ai_service is None:
        try:
            ai_service = AIService()
        except ValueError as e:
            raise HTTPException(
                status_code=500, 
                detail=str(e)
            )
    return ai_service

class JobRequirement(BaseModel):
    job_title: str
    job_description: str
    required_skills: Optional[str] = ""
    experience_level: Optional[str] = ""

class ResumeAnalysisResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str = ""

@app.get("/")
async def root():
    return {"message": "AI Resume Analyzer API", "version": "1.0.0"}

@app.post("/api/upload-resume", response_model=ResumeAnalysisResponse)
async def upload_resume(file: UploadFile = File(...)):
    """上传并解析简历 - 使用AI分析"""
    try:
        # 验证文件类型
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="只支持PDF格式文件")
        
        # 读取文件内容
        content = await file.read()
        
        # 解析PDF
        text_content = pdf_parser.extract_text(content)
        
        if not text_content or len(text_content) < 50:
            raise HTTPException(status_code=400, detail="PDF文件内容为空或无法解析")
        
        # 使用AI提取关键信息
        ai = get_ai_service()
        extracted_info = ai.extract_resume_info(text_content)
        
        # 缓存结果
        resume_id = cache_manager.cache_resume(extracted_info, text_content)
        
        return ResumeAnalysisResponse(
            success=True,
            data={
                "resume_id": resume_id,
                "extracted_info": extracted_info,
                "text_preview": text_content[:500] + "..." if len(text_content) > 500 else text_content
            },
            message="简历解析成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        return ResumeAnalysisResponse(
            success=False,
            message=f"简历解析失败: {str(e)}"
        )

@app.post("/api/match-job", response_model=ResumeAnalysisResponse)
async def match_job(request_data: dict):
    """简历与岗位匹配评分 - 使用AI分析"""
    try:
        # 从请求中提取数据
        resume_id = request_data.get("resume_id")
        if not resume_id:
            raise HTTPException(status_code=400, detail="缺少resume_id参数")
        
        # 构建岗位需求对象
        job_req = JobRequirement(
            job_title=request_data.get("job_title", ""),
            job_description=request_data.get("job_description", ""),
            required_skills=request_data.get("required_skills", ""),
            experience_level=request_data.get("experience_level", "")
        )
        
        # 从缓存获取简历信息
        resume_data = cache_manager.get_resume(resume_id)
        if not resume_data:
            raise HTTPException(status_code=404, detail="简历数据未找到，请重新上传")
        
        # 使用AI进行匹配评分
        ai = get_ai_service()
        match_result = ai.analyze_job_match(
            resume_data["extracted_info"],
            job_req.dict()
        )
        
        return ResumeAnalysisResponse(
            success=True,
            data=match_result,
            message="匹配评分完成"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        return ResumeAnalysisResponse(
            success=False,
            message=f"匹配评分失败: {str(e)}"
        )

@app.get("/api/resume/{resume_id}", response_model=ResumeAnalysisResponse)
async def get_resume(resume_id: str):
    """获取简历信息"""
    try:
        resume_data = cache_manager.get_resume(resume_id)
        if not resume_data:
            raise HTTPException(status_code=404, detail="简历数据未找到")
        
        return ResumeAnalysisResponse(
            success=True,
            data=resume_data,
            message="获取简历信息成功"
        )
        
    except Exception as e:
        return ResumeAnalysisResponse(
            success=False,
            message=f"获取简历信息失败: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)