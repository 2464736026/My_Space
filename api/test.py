"""
测试端点 - 检查环境变量
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@app.get("/api/test")
async def test_env():
    """测试环境变量是否正确加载"""
    
    api_key = os.getenv("OPENAI_API_KEY", "")
    
    env_vars = {
        "status": "ok",
        "OPENAI_API_KEY": "exists" if api_key else "missing",
        "OPENAI_API_KEY_length": len(api_key) if api_key else 0,
        "OPENAI_API_KEY_preview": api_key[:10] + "..." if len(api_key) > 10 else api_key,
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "not set"),
        "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", "not set"),
        "env_count": len(os.environ.keys())
    }
    
    return env_vars

# Vercel handler
from mangum import Mangum
handler = Mangum(app, lifespan="off")
