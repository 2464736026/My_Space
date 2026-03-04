"""
使用Vercel原生Python支持，不使用Mangum
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # 根路径
        if path == '/' or path == '':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "AI Resume Analyzer API",
                "version": "1.0.0",
                "status": "running",
                "endpoints": ["/api/upload-resume", "/api/match-job"]
            }
            self.wfile.write(json.dumps(response).encode())
            return
        
        # 健康检查
        if path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            api_key = os.getenv("OPENAI_API_KEY", "")
            response = {
                "status": "healthy",
                "openai_configured": bool(api_key and len(api_key) > 20),
                "openai_model": os.getenv("OPENAI_MODEL", "not set"),
                "openai_base_url": os.getenv("OPENAI_BASE_URL", "not set")
            }
            self.wfile.write(json.dumps(response).encode())
            return
        
        # 环境变量测试
        if path == '/api/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            api_key = os.getenv("OPENAI_API_KEY", "")
            response = {
                "status": "ok",
                "OPENAI_API_KEY": "exists" if api_key else "missing",
                "OPENAI_API_KEY_length": len(api_key) if api_key else 0,
                "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "not set"),
                "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", "not set")
            }
            self.wfile.write(json.dumps(response).encode())
            return
        
        # 404
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_POST(self):
        """处理POST请求"""
        self.send_response(501)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "POST not implemented yet"}).encode())
    
    def do_OPTIONS(self):
        """处理OPTIONS请求（CORS预检）"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
