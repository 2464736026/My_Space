# -*- coding: utf-8 -*-
"""
阿里云函数计算入口 - 兼容多种触发器格式
"""
import sys
import os
import json

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def handler(event, context):
    """
    阿里云 FC 统一处理函数
    自动检测是 HTTP 触发器还是事件触发器
    """
    try:
        # 检查是否是 WSGI 格式（HTTP 触发器的旧格式）
        # 如果 event 是 dict 且包含 environ 相关的键
        if isinstance(event, dict) and 'REQUEST_METHOD' in str(event):
            return handle_http_event(event, context)
        
        # 检查是否是标准 HTTP 事件格式
        if isinstance(event, (dict, str, bytes)):
            return handle_http_event(event, context)
        
        # 默认返回健康检查
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'message': 'AI Resume Analyzer API',
                'version': '1.0.0',
                'status': 'healthy'
            })
        }
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Handler Error: {error_detail}")
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'success': False,
                'error': str(e),
                'message': 'Internal Server Error',
                'detail': error_detail
            })
        }


def handle_http_event(event, context):
    """处理 HTTP 事件"""
    try:
        # 导入 FastAPI 应用
        from app.main import app
        from starlette.testclient import TestClient
        
        # 创建测试客户端
        client = TestClient(app)
        
        # 解析事件
        if isinstance(event, bytes):
            event = json.loads(event.decode('utf-8'))
        elif isinstance(event, str):
            event = json.loads(event)
        
        # 获取请求信息
        method = event.get('method', event.get('httpMethod', 'GET')).upper()
        path = event.get('path', event.get('requestPath', '/'))
        query_string = event.get('queryString', event.get('queryParameters', ''))
        headers = event.get('headers', event.get('requestHeaders', {}))
        body = event.get('body', '')
        
        # 构建完整路径
        if query_string:
            if isinstance(query_string, dict):
                # 如果是字典，转换为查询字符串
                query_parts = [f"{k}={v}" for k, v in query_string.items()]
                query_string = '&'.join(query_parts)
            full_path = f"{path}?{query_string}"
        else:
            full_path = path
        
        # 处理请求体
        if isinstance(body, str):
            request_body = body.encode('utf-8')
        else:
            request_body = body if body else b''
        
        # 调用 FastAPI 应用
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
        else:
            response = client.get(full_path, headers=headers)
        
        # 构建响应
        return {
            'statusCode': response.status_code,
            'headers': {
                'Content-Type': response.headers.get('content-type', 'application/json'),
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': '*',
            },
            'body': response.text
        }
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"HTTP Handler Error: {error_detail}")
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'success': False,
                'error': str(e),
                'message': 'Internal Server Error',
                'detail': error_detail
            })
        }
