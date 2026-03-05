"""
调试版本 - 测试Vercel路由
"""
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, data):
        """发送响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_GET(self):
        """处理GET请求"""
        self._send_response(200, {
            "method": "GET",
            "path": self.path,
            "message": "Debug endpoint working"
        })
    
    def do_POST(self):
        """处理POST请求"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''
        
        self._send_response(200, {
            "method": "POST",
            "path": self.path,
            "content_type": self.headers.get('Content-Type', ''),
            "content_length": content_length,
            "message": "POST request received successfully"
        })
    
    def do_OPTIONS(self):
        """处理OPTIONS请求"""
        self._send_response(200, {
            "method": "OPTIONS",
            "message": "CORS preflight OK"
        })
