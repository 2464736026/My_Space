#!/usr/bin/env python3
"""
开发环境启动脚本
同时启动前端和后端服务
"""

import subprocess
import sys
import os
import time
import threading

def run_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    os.chdir("backend")
    
    # 检查依赖
    try:
        subprocess.run([sys.executable, "-c", "import fastapi, uvicorn"], check=True)
    except subprocess.CalledProcessError:
        print("📦 安装后端依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # 启动后端
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--reload", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

def run_frontend():
    """启动前端服务"""
    print("🎨 启动前端服务...")
    os.chdir("frontend")
    
    # 检查node_modules
    if not os.path.exists("node_modules"):
        print("📦 安装前端依赖...")
        subprocess.run(["npm", "install"], check=True)
    
    # 启动前端
    subprocess.run(["npm", "run", "dev"])

def main():
    """主函数"""
    print("🔥 启动AI智能简历分析系统开发环境")
    print("=" * 50)
    
    # 检查目录结构
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ 项目目录结构不正确")
        print("请确保在项目根目录运行此脚本")
        return
    
    try:
        # 创建线程启动后端
        backend_thread = threading.Thread(target=run_backend)
        backend_thread.daemon = True
        backend_thread.start()
        
        # 等待后端启动
        time.sleep(3)
        
        # 启动前端（主线程）
        run_frontend()
        
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")

if __name__ == "__main__":
    main()