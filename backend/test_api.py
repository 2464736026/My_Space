#!/usr/bin/env python3
"""
API测试脚本
用于测试后端API功能
"""

import requests
import json
import os

# API基础URL
BASE_URL = "http://localhost:8000"

def test_root():
    """测试根路径"""
    print("测试根路径...")
    response = requests.get(f"{BASE_URL}/")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print("-" * 50)

def test_upload_resume():
    """测试简历上传（需要PDF文件）"""
    print("测试简历上传...")
    
    # 创建一个测试PDF文件路径
    test_pdf_path = "test_resume.pdf"
    
    if not os.path.exists(test_pdf_path):
        print(f"测试PDF文件 {test_pdf_path} 不存在，跳过上传测试")
        return None
    
    with open(test_pdf_path, 'rb') as f:
        files = {'file': ('test_resume.pdf', f, 'application/pdf')}
        response = requests.post(f"{BASE_URL}/api/upload-resume", files=files)
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    if result.get('success'):
        return result['data']['resume_id']
    
    print("-" * 50)
    return None

def test_job_match(resume_id):
    """测试岗位匹配"""
    if not resume_id:
        print("没有简历ID，跳过匹配测试")
        return
    
    print("测试岗位匹配...")
    
    job_data = {
        "job_title": "Python后端开发工程师",
        "job_description": "负责后端API开发，使用Python、FastAPI、MySQL等技术栈",
        "required_skills": "Python, FastAPI, MySQL, Redis, Docker",
        "experience_level": "3年以上工作经验"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/match-job",
        params={"resume_id": resume_id},
        json=job_data
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print("-" * 50)

def main():
    """主测试函数"""
    print("开始API测试...")
    print("=" * 50)
    
    try:
        # 测试根路径
        test_root()
        
        # 测试简历上传
        resume_id = test_upload_resume()
        
        # 测试岗位匹配
        test_job_match(resume_id)
        
        print("测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("连接失败！请确保后端服务正在运行 (python -m uvicorn app.main:app --reload)")
    except Exception as e:
        print(f"测试出错: {str(e)}")

if __name__ == "__main__":
    main()