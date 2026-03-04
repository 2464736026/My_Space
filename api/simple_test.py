"""
最简单的测试 - 不依赖任何复杂库
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
async def root():
    return {
        "status": "ok",
        "message": "Simple test endpoint working",
        "python_version": os.sys.version
    }

@app.get("/env")
async def check_env():
    return {
        "OPENAI_API_KEY": "exists" if os.getenv("OPENAI_API_KEY") else "missing",
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "not set"),
        "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", "not set")
    }

# Vercel handler
from mangum import Mangum
handler = Mangum(app, lifespan="off")
