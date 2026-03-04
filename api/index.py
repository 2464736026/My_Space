"""
Vercel Serverless Function Entry Point
"""
import sys
import os

# 添加 backend 目录到路径
backend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
sys.path.insert(0, backend_dir)

from app.main import app
from mangum import Mangum

# Vercel 需要的 handler
handler = Mangum(app, lifespan="off")
