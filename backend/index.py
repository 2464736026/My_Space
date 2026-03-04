# -*- coding: utf-8 -*-
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入 FastAPI 应用
from app.main import app

# 阿里云函数计算需要的 WSGI handler
# 直接使用 Mangum 适配器将 ASGI 应用转换为 WSGI
try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except ImportError:
    # 如果没有 mangum，使用简单的 WSGI 适配器
    from starlette.testclient import TestClient
    
    def handler(environ, start_response):
        """简单的 WSGI handler"""
        client = TestClient(app)
        
        method = environ.get('REQUEST_METHOD', 'GET')
        path = environ.get('PATH_INFO', '/')
        query = environ.get('QUERY_STRING', '')
        
        url = path
        if query:
            url = f"{path}?{query}"
        
        # 读取请求体
        try:
            length = int(environ.get('CONTENT_LENGTH', 0))
        except:
            length = 0
        
        body = environ['wsgi.input'].read(length) if length > 0 else b''
        
        # 构建请求头
        headers = {}
        for k, v in environ.items():
            if k.startswith('HTTP_'):
                headers[k[5:].replace('_', '-')] = v
        
        if 'CONTENT_TYPE' in environ:
            headers['Content-Type'] = environ['CONTENT_TYPE']
        
        # 调用 FastAPI
        if method == 'GET':
            resp = client.get(url, headers=headers)
        elif method == 'POST':
            resp = client.post(url, content=body, headers=headers)
        elif method == 'PUT':
            resp = client.put(url, content=body, headers=headers)
        elif method == 'DELETE':
            resp = client.delete(url, headers=headers)
        elif method == 'OPTIONS':
            resp = client.options(url, headers=headers)
        else:
            resp = client.get(url, headers=headers)
        
        # 构建响应
        status = f"{resp.status_code} OK"
        response_headers = [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', '*'),
            ('Access-Control-Allow-Headers', '*'),
        ]
        
        for k, v in resp.headers.items():
            if k.lower() not in ['content-length', 'transfer-encoding']:
                response_headers.append((k, v))
        
        start_response(status, response_headers)
        return [resp.content]
