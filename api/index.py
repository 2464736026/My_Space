"""
Vercel Serverless Function Entry Point
"""
import sys
from pathlib import Path

# 添加项目根目录和 backend 目录到 Python 路径
current_dir = Path(__file__).parent
root_dir = current_dir.parent
backend_dir = root_dir / 'backend'

# 确保路径存在
if backend_dir.exists():
    sys.path.insert(0, str(backend_dir))
    sys.path.insert(0, str(root_dir))

try:
    from app.main import app
    from mangum import Mangum
    
    # Vercel handler
    handler = Mangum(app, lifespan="off")
except Exception as e:
    # 如果导入失败，创建一个简单的错误处理函数
    def handler(event, context):
        return {
            'statusCode': 500,
            'body': f'Import Error: {str(e)}\nPython Path: {sys.path}\nBackend Dir: {backend_dir}'
        }
