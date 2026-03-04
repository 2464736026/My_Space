# -*- coding: utf-8 -*-
"""
阿里云函数计算入口 - 事件函数格式
"""
import sys
import os
import json

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def handler(event, context):
    """
    阿里云 FC 事件函数处理器
    
    Args:
        event: 事件对象，包含请求信息
        context: 上下文对象，包含函数运行时信息
    
    Returns:
        dict: HTTP 响应对象
    """
    try:
        # 导入 FastAPI 应用
        from app.main import app
        from starlette.testclient import TestClient
        
        # 创建测试客户端
        client = TestClient(app)
        
        # 解析事件对象
        # 阿里云 FC HTTP 触发器会将请求信息放在 event 中
        if isinstance(event, bytes):
            event = json.loads(event.decode('utf-8'))
        elif isinstance(event, str):
            event = json.loads(event)
        
        # 获取请求信息
        method = event.get('method', 'GET').upper()
        path = event.get('path', '/')
        query_string = event.get('queryString', '')
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        # 构建完整路径
        if query_string:
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
        
        # 构建响应对象
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
        # 错误处理
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
                'message': 'Internal Server Error'
            })
        }
