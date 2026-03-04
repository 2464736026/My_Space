import sys
import os

# 添加 backend 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend'))

# 导入应用
from app.main import app

# 导出 app 供 Vercel 使用
# Vercel 会自动使用 Mangum 包装
