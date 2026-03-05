# PDF上传问题诊断指南

## 📋 问题描述

前端已成功部署，界面功能正常，但提交PDF时出现报错，无法识别PDF文档。

## 🔍 可能的原因

### 1. CORS跨域问题
前端（https://my-space-frontend.vercel.app）调用后端API（https://my-space-beryl.vercel.app）时可能遇到跨域限制。

### 2. PDF文件解析失败
- PDF文件格式不支持
- PDF内容为空或加密
- PDF解析库问题

### 3. OpenAI API调用失败
- API Key配置问题
- API请求超时
- API返回格式错误

### 4. 文件上传大小限制
- Vercel有请求体大小限制（默认4.5MB）
- PDF文件过大

## 🛠️ 诊断步骤

### 步骤1：检查浏览器控制台错误

请提供以下信息：

1. **打开浏览器开发者工具**（F12）
2. **切换到Console标签**
3. **上传PDF文件**
4. **复制所有红色错误信息**

需要的信息：
```
- 错误类型（Network Error / CORS / 500 / 400等）
- 错误详细信息
- 请求URL
- 响应状态码
```

### 步骤2：检查Network请求

1. **切换到Network标签**
2. **上传PDF文件**
3. **找到 `/api/upload-resume` 请求**
4. **查看以下信息：**
   - Status Code（状态码）
   - Response（响应内容）
   - Request Headers（请求头）
   - Request Payload（请求体）

### 步骤3：测试后端API健康状态

在浏览器中访问以下URL：

```
https://my-space-beryl.vercel.app/api/health
```

**预期响应：**
```json
{
  "status": "healthy",
  "openai_configured": true,
  "openai_model": "gpt-3.5-turbo",
  "openai_base_url": "https://api.openai-proxy.org/v1"
}
```

### 步骤4：测试环境变量配置

访问：
```
https://my-space-beryl.vercel.app/api/test
```

**预期响应：**
```json
{
  "status": "ok",
  "OPENAI_API_KEY": "exists",
  "OPENAI_API_KEY_length": 48,
  "OPENAI_MODEL": "gpt-3.5-turbo",
  "OPENAI_BASE_URL": "https://api.openai-proxy.org/v1"
}
```

## 🔧 常见问题及解决方案

### 问题1：CORS错误

**错误信息：**
```
Access to XMLHttpRequest at 'https://my-space-beryl.vercel.app/api/upload-resume' 
from origin 'https://my-space-frontend.vercel.app' has been blocked by CORS policy
```

**解决方案：**
后端已配置CORS，但可能需要重新部署。

### 问题2：PDF解析失败

**错误信息：**
```
{
  "success": false,
  "message": "PDF文件内容为空或无法解析"
}
```

**可能原因：**
- PDF文件是扫描件（图片格式）
- PDF文件加密
- PDF文件损坏

**解决方案：**
- 使用文本型PDF（可复制文字的PDF）
- 确保PDF未加密
- 尝试其他PDF文件

### 问题3：OpenAI API调用失败

**错误信息：**
```
{
  "success": false,
  "message": "AI简历分析失败: ..."
}
```

**可能原因：**
- API Key无效或过期
- API请求超时
- API返回格式错误

**解决方案：**
检查Vercel环境变量配置。

### 问题4：文件过大

**错误信息：**
```
413 Payload Too Large
```

**解决方案：**
- 压缩PDF文件
- 限制文件大小在4MB以内

### 问题5：网络超时

**错误信息：**
```
Network Error / Timeout
```

**解决方案：**
- 检查网络连接
- 增加请求超时时间
- 重试上传

## 📝 需要提供的信息

为了更好地诊断问题，请提供：

1. **浏览器控制台的完整错误信息**（截图或文字）
2. **Network标签中 `/api/upload-resume` 请求的详细信息**
3. **访问 `/api/health` 的响应结果**
4. **访问 `/api/test` 的响应结果**
5. **使用的PDF文件信息**：
   - 文件大小
   - 是否可以复制文字
   - 是否加密

## 🧪 测试用例

### 测试1：使用简单文本PDF

创建一个简单的测试PDF：
1. 打开Word或记事本
2. 输入以下内容：
```
姓名：张三
电话：13800138000
邮箱：zhangsan@example.com
求职意向：Python工程师
工作经验：3年
技能：Python, Django, MySQL
```
3. 另存为PDF
4. 上传测试

### 测试2：使用curl测试后端

```bash
# 测试健康检查
curl https://my-space-beryl.vercel.app/api/health

# 测试环境变量
curl https://my-space-beryl.vercel.app/api/test
```

## 🚀 快速修复建议

### 方案1：检查前端API地址配置

确认 `frontend/src/App.jsx` 中的API地址：
```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://my-space-beryl.vercel.app' 
  : 'http://localhost:8000';
```

### 方案2：检查后端CORS配置

确认 `api/index.py` 中的CORS头：
```python
self.send_header('Access-Control-Allow-Origin', '*')
```

### 方案3：增加错误日志

在前端添加详细的错误日志：
```javascript
catch (error) {
  console.error('Upload error:', error);
  console.error('Error response:', error.response?.data);
  console.error('Error status:', error.response?.status);
}
```

## 📞 下一步

请按照以下顺序操作：

1. ✅ 访问 `/api/health` 和 `/api/test` 端点
2. ✅ 打开浏览器开发者工具
3. ✅ 上传PDF文件
4. ✅ 复制所有错误信息
5. ✅ 提供给我进行分析

---

**准备好后，请提供上述信息，我将帮你精准定位问题！** 🎯
