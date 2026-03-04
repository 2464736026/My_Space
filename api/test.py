"""
Simple test endpoint to verify Vercel deployment
"""
import sys
import os

def handler(event, context):
    """Simple test handler"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': {
            'message': 'Test endpoint working!',
            'python_version': sys.version,
            'python_path': sys.path,
            'env_vars': {
                'OPENAI_API_KEY': 'exists' if os.getenv('OPENAI_API_KEY') else 'missing',
                'OPENAI_MODEL': os.getenv('OPENAI_MODEL', 'not set'),
                'OPENAI_BASE_URL': os.getenv('OPENAI_BASE_URL', 'not set'),
            },
            'current_dir': os.getcwd(),
            'files': os.listdir('.')
        }
    }
