"""
阿里云函数计算入口文件
支持 HTTP 触发器
"""
import json
import sys
import os
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

def handler(environ, start_response):
    """
    阿里云函数计算 WSGI 处理函数
    兼容 FC HTTP 触发器
    """
    try:
        # 导入 FastAPI 应用
        from app.main import app
        
        # 获取请求信息
        method = environ.get('REQUEST_METHOD', 'GET')
        path = environ.get('PATH_INFO', '/')
        query_string = environ.get('QUERY_STRING', '')
        
        # 构建完整URL路径
        if query_string:
            full_path = f"{path}?{query_string}"
        else:
            full_path = path
        
        # 读取请求体
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError, TypeError):
            content_length = 0
        
        request_body = b''
        if content_length > 0:
            try:
                request_body = environ['wsgi.input'].read(content_length)
            except Exception:
                request_body = b''
        
        # 构建请求头
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                # 转换 HTTP_XXX 为标准头格式
                header_name = key[5:].replace('_', '-').lower()
                headers[header_name] = value
        
        # 添加 Content-Type
        if 'CONTENT_TYPE' in environ and environ['CONTENT_TYPE']:
            headers['content-type'] = environ['CONTENT_TYPE']
        
        # 使用 TestClient 调用 FastAPI
        from starlette.testclient import TestClient
        client = TestClient(app)
        
        # 根据方法调用对应的接口
        try:
            if method == 'GET':
                response = client.get(full_path, headers=headers)
            elif method == 'POST':
                response = client.post(full_path, content=request_body, headers=headers)
            elif method == 'PUT':
                response = client.put(full_path, content=request_body, headers=headers)
            elif method == 'DELETE':
                response = client.delete(full_path, headers=headers)
            elif method == 'OPTIONS':
                response = client.options(full_path, headers=headers)
            elif method == 'PATCH':
                response = client.patch(full_path, content=request_body, headers=headers)
            elif method == 'HEAD':
                response = client.head(full_path, headers=headers)
            else:
                # 默认使用 GET
                response = client.get(full_path, headers=headers)
        except Exception as e:
            # 如果调用失败，返回错误
            return _error_response(start_response, str(e), 500)
        
        # 构建响应状态
        status_code = response.status_code
        status_text = _get_status_text(status_code)
        status = f'{status_code} {status_text}'
        
        # 构建响应头
        response_headers = []
        
        # 添加 CORS 头（允许跨域）
        response_headers.append(('Access-Control-Allow-Origin', '*'))
        response_headers.append(('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD'))
        response_headers.append(('Access-Control-Allow-Headers', '*'))
        response_headers.append(('Access-Control-Max-Age', '86400'))
        
        # 添加日期头（阿里云 FC 需要）
        response_headers.append(('Date', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')))
        
        # 添加其他响应头
        for key, value in response.headers.items():
            key_lower = key.lower()
            # 跳过某些头
            if key_lower not in ['content-length', 'transfer-encoding', 'connection']:
                response_headers.append((key, value))
        
        # 设置响应
        start_response(status, response_headers)
        
        # 返回响应体
        return [response.content]
        
    except Exception as e:
        # 顶层错误处理
        import traceback
        error_detail = traceback.format_exc()
        print(f"Handler Error: {error_detail}")
        return _error_response(start_response, str(e), 500)


def _get_status_text(status_code):
    """获取 HTTP 状态码对应的文本"""
    status_texts = {
        200: 'OK',
        201: 'Created',
        204: 'No Content',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        422: 'Unprocessable Entity',
        500: 'Internal Server Error',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
    }
    return status_texts.get(status_code, 'Unknown')


def _error_response(start_response, error_message, status_code=500):
    """返回错误响应"""
    error_data = {
        "success": False,
        "error": error_message,
        "message": "Internal Server Error",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    status_text = _get_status_text(status_code)
    status = f'{status_code} {status_text}'
    
    response_headers = [
        ('Content-Type', 'application/json; charset=utf-8'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
        ('Access-Control-Allow-Headers', '*'),
        ('Date', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'))
    ]
    
    start_response(status, response_headers)
    return [json.dumps(error_data, ensure_ascii=False).encode('utf-8')]
