"""
最小化测试 - 只测试FastAPI + Mangum是否工作
"""
from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Minimal test working"}

@app.get("/api/env")
def env():
    return {
        "OPENAI_API_KEY": "set" if os.getenv("OPENAI_API_KEY") else "not set",
        "env_vars": len(os.environ)
    }

from mangum import Mangum
handler = Mangum(app, lifespan="off")
