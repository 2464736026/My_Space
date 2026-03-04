"""
Vercel Serverless Function Entry Point
"""
import sys
import os

# 添加 backend 目录到 Python 路径
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# 导入 FastAPI 应用
from app.main import app
from mangum import Mangum

# Vercel handler
handler = Mangum(app, lifespan="off")
