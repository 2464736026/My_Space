"""
测试端点 - 检查环境变量
"""
import os
import json

def handler(event, context):
    """测试环境变量是否正确加载"""
    
    env_vars = {
        "OPENAI_API_KEY": "exists" if os.getenv("OPENAI_API_KEY") else "missing",
        "OPENAI_API_KEY_length": len(os.getenv("OPENAI_API_KEY", "")) if os.getenv("OPENAI_API_KEY") else 0,
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "not set"),
        "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", "not set"),
        "all_env_keys": list(os.environ.keys())
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps(env_vars, ensure_ascii=False)
    }
