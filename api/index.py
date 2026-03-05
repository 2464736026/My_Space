"""
Vercel原生Python Handler - 完整版本
支持简历上传和岗位匹配功能
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import os
import sys
import traceback
import io

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

# 全局变量
pdf_parser = None
cache_manager = None
ai_service = None

def lazy_import():
    """延迟导入依赖模块"""
    global pdf_parser, cache_manager, ai_service
    
    if pdf_parser is None:
        try:
            from services.pdf_parser import PDFParser
            from services.ai_service import AIService
            from utils.cache import CacheManager
            
            pdf_parser = PDFParser()
            cache_manager = CacheManager()
            ai_service = AIService()
            
            print("Successfully imported all services")
        except Exception as e:
            print(f"Import error: {e}")
            print(traceback.format_exc())
            raise

class handler(BaseHTTPRequestHandler):
    def _send_json_response(self, status_code, data):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # 根路径
        if path == '/' or path == '':
            response = {
                "message": "AI Resume Analyzer API",
                "version": "1.0.0",
                "status": "running",
                "endpoints": ["/api/upload-resume", "/api/match-job", "/api/health", "/api/test"]
            }
            self._send_json_response(200, response)
            return
        
        # 健康检查
        if path == '/api/health':
            try:
                api_key = os.getenv("OPENAI_API_KEY", "")
                response = {
                    "status": "healthy",
                    "openai_configured": bool(api_key and len(api_key) > 20),
                    "openai_model": os.getenv("OPENAI_MODEL", "not set"),
                    "openai_base_url": os.getenv("OPENAI_BASE_URL", "not set")
                }
                self._send_json_response(200, response)
            except Exception as e:
                self._send_json_response(500, {
                    "status": "unhealthy",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                })
            return
        
        # 环境变量测试
        if path == '/api/test':
            api_key = os.getenv("OPENAI_API_KEY", "")
            response = {
                "status": "ok",
                "OPENAI_API_KEY": "exists" if api_key else "missing",
                "OPENAI_API_KEY_length": len(api_key) if api_key else 0,
                "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "not set"),
                "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", "not set")
            }
            self._send_json_response(200, response)
            return
        
        # 404
        self._send_json_response(404, {"error": "Not found"})
    
    def do_POST(self):
        """处理POST请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            # 上传简历
            if path == '/api/upload-resume':
                self._handle_upload_resume()
                return
            
            # 岗位匹配
            if path == '/api/match-job':
                self._handle_match_job()
                return
            
            # 404
            self._send_json_response(404, {"error": "Not found"})
            
        except Exception as e:
            print(f"POST error: {str(e)}")
            print(traceback.format_exc())
            self._send_json_response(500, {
                "success": False,
                "message": f"服务器错误: {str(e)}"
            })
    
    def _handle_upload_resume(self):
        """处理简历上传"""
        try:
            print("=== Starting upload_resume handler ===")
            
            # 确保服务已导入
            try:
                print("Attempting to import services...")
                lazy_import()
                print("Services imported successfully")
            except Exception as import_error:
                print(f"Import error: {str(import_error)}")
                print(traceback.format_exc())
                self._send_json_response(500, {
                    "success": False,
                    "message": f"服务初始化失败: {str(import_error)}",
                    "error_type": "import_error"
                })
                return
            
            # 读取multipart/form-data
            content_type = self.headers.get('Content-Type', '')
            print(f"Content-Type: {content_type}")
            
            if 'multipart/form-data' not in content_type:
                self._send_json_response(400, {
                    "success": False,
                    "message": "Content-Type must be multipart/form-data"
                })
                return
            
            # 获取boundary
            try:
                boundary = content_type.split('boundary=')[1].encode()
                print(f"Boundary extracted: {boundary[:20]}...")
            except Exception as boundary_error:
                print(f"Boundary extraction error: {str(boundary_error)}")
                self._send_json_response(400, {
                    "success": False,
                    "message": "无法解析boundary"
                })
                return
            
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            print(f"Content-Length: {content_length}")
            body = self.rfile.read(content_length)
            print(f"Body read: {len(body)} bytes")
            
            # 解析multipart数据
            parts = body.split(b'--' + boundary)
            print(f"Found {len(parts)} parts")
            
            pdf_content = None
            filename = None
            
            for i, part in enumerate(parts):
                if b'Content-Disposition' in part and b'filename=' in part:
                    print(f"Found file in part {i}")
                    # 提取文件名
                    lines = part.split(b'\r\n')
                    for line in lines:
                        if b'filename=' in line:
                            filename = line.decode('utf-8', errors='ignore').split('filename="')[1].split('"')[0]
                            print(f"Filename: {filename}")
                            break
                    
                    # 提取文件内容
                    content_start = part.find(b'\r\n\r\n') + 4
                    content_end = len(part) - 2  # 移除末尾的\r\n
                    pdf_content = part[content_start:content_end]
                    print(f"PDF content extracted: {len(pdf_content)} bytes")
                    break
            
            if not pdf_content or not filename:
                print("ERROR: No PDF content or filename found")
                self._send_json_response(400, {
                    "success": False,
                    "message": "未找到PDF文件"
                })
                return
            
            if not filename.lower().endswith('.pdf'):
                print(f"ERROR: Not a PDF file: {filename}")
                self._send_json_response(400, {
                    "success": False,
                    "message": "只支持PDF格式文件"
                })
                return
            
            print(f"Processing file: {filename}, size: {len(pdf_content)} bytes")
            
            # 解析PDF
            try:
                print("Starting PDF extraction...")
                text_content = pdf_parser.extract_text(pdf_content)
                print(f"PDF extraction successful. Text length: {len(text_content)}")
                print(f"Text preview: {text_content[:200]}...")
            except Exception as pdf_error:
                print(f"PDF extraction error: {str(pdf_error)}")
                print(traceback.format_exc())
                self._send_json_response(500, {
                    "success": False,
                    "message": f"PDF解析失败: {str(pdf_error)}",
                    "error_type": "pdf_parse_error"
                })
                return
            
            if not text_content or len(text_content) < 50:
                print(f"ERROR: Text content too short: {len(text_content)} chars")
                self._send_json_response(400, {
                    "success": False,
                    "message": "PDF文件内容为空或无法解析"
                })
                return
            
            # AI提取信息
            try:
                print("Starting AI extraction...")
                extracted_info = ai_service.extract_resume_info(text_content)
                print(f"AI extraction successful: {extracted_info}")
            except Exception as ai_error:
                print(f"AI extraction error: {str(ai_error)}")
                print(traceback.format_exc())
                self._send_json_response(500, {
                    "success": False,
                    "message": f"AI分析失败: {str(ai_error)}",
                    "error_type": "ai_error"
                })
                return
            
            # 缓存简历
            try:
                print("Caching resume...")
                resume_id = cache_manager.cache_resume(extracted_info, text_content)
                print(f"Resume cached with ID: {resume_id}")
            except Exception as cache_error:
                print(f"Cache error: {str(cache_error)}")
                print(traceback.format_exc())
                self._send_json_response(500, {
                    "success": False,
                    "message": f"缓存失败: {str(cache_error)}",
                    "error_type": "cache_error"
                })
                return
            
            # 返回结果
            print("=== Upload successful ===")
            self._send_json_response(200, {
                "success": True,
                "data": {
                    "resume_id": resume_id,
                    "extracted_info": extracted_info,
                    "text_preview": text_content[:500] + "..." if len(text_content) > 500 else text_content
                },
                "message": "简历解析成功"
            })
            
        except Exception as e:
            print(f"=== FATAL ERROR in upload_resume ===")
            print(f"Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            print(traceback.format_exc())
            self._send_json_response(500, {
                "success": False,
                "message": f"服务器错误: {str(e)}",
                "error_type": type(e).__name__
            })
    
    def _handle_match_job(self):
        """处理岗位匹配"""
        try:
            # 确保服务已导入
            lazy_import()
            
            # 读取JSON数据
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            request_data = json.loads(body.decode('utf-8'))
            
            resume_id = request_data.get("resume_id")
            if not resume_id:
                self._send_json_response(400, {
                    "success": False,
                    "message": "缺少resume_id参数"
                })
                return
            
            # 获取缓存的简历
            resume_data = cache_manager.get_resume(resume_id)
            if not resume_data:
                self._send_json_response(404, {
                    "success": False,
                    "message": "简历数据未找到"
                })
                return
            
            # 构建岗位需求
            job_req = {
                "job_title": request_data.get("job_title", ""),
                "job_description": request_data.get("job_description", ""),
                "required_skills": request_data.get("required_skills", ""),
                "experience_level": request_data.get("experience_level", "")
            }
            
            # AI匹配分析
            match_result = ai_service.analyze_job_match(
                resume_data["extracted_info"],
                job_req
            )
            
            # 返回结果
            self._send_json_response(200, {
                "success": True,
                "data": match_result,
                "message": "匹配评分完成"
            })
            
        except Exception as e:
            print(f"Error in match_job: {str(e)}")
            print(traceback.format_exc())
            self._send_json_response(500, {
                "success": False,
                "message": f"匹配评分失败: {str(e)}"
            })
    
    def do_OPTIONS(self):
        """处理OPTIONS请求（CORS预检）"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
