# -*- coding: utf-8 -*-
"""
阿里云函数计算入口 - 使用 a2wsgi 适配器
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入 FastAPI 应用
from app.main import app

# 使用 a2wsgi 将 ASGI 应用转换为 WSGI
try:
    from a2wsgi import ASGIMiddleware
    # 创建 WSGI 应用
    application = ASGIMiddleware(app)
    # 阿里云 FC 需要的 handler
    handler = application
except ImportError:
    # 如果没有 a2wsgi，使用备用方案
    print("Warning: a2wsgi not found, using fallback handler")
    
    def handler(environ, start_response):
        """备用 WSGI handler"""
        import json
        from datetime import datetime
        
        # 简单的健康检查响应
        path = environ.get('PATH_INFO', '/')
        
        if path == '/' or path == '':
            response_body = json.dumps({
                "message": "AI Resume Analyzer API",
                "version": "1.0.0"
            }).encode('utf-8')
            
            status = '200 OK'
            response_headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(response_body))),
                ('Access-Control-Allow-Origin', '*'),
            ]
            
            start_response(status, response_headers)
            return [response_body]
        else:
            # 其他路径返回404
            response_body = json.dumps({
                "error": "Not Found",
                "message": "Please install a2wsgi: pip install a2wsgi"
            }).encode('utf-8')
            
            status = '404 Not Found'
            response_headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(response_body))),
                ('Access-Control-Allow-Origin', '*'),
            ]
            
            start_response(status, response_headers)
            return [response_body]
