# Vercel 部署问题诊断指南

## 已完成的修复

### 1. 代码改进
- ✅ 修复了 `api/test.py` 的handler格式（从AWS Lambda格式改为FastAPI + Mangum）
- ✅ 在 `api/index.py` 中添加了详细的错误日志和traceback
- ✅ 在 `api/services/ai_service.py` 中添加了详细的初始化日志
- ✅ 添加了 `/api/health` 健康检查端点
- ✅ 改进了导入错误处理
- ✅ 更新了 `vercel.json` 配置，增加了PYTHONPATH和maxLambdaSize
- ✅ 创建了 `.vercelignore` 文件排除不必要的文件

### 2. 代码已推送到GitHub
- 仓库：https://github.com/2464736026/My_Space
- 最新commit：Fix Vercel deployment: improve error handling, logging, and routing

## 下一步操作（请按顺序执行）

### 步骤1：触发Vercel重新部署

由于代码已更新，Vercel应该会自动检测到GitHub的push并触发新的部署。

1. 打开 Vercel Dashboard：https://vercel.com/dashboard
2. 找到你的项目 `my-space`
3. 查看 "Deployments" 标签页
4. 等待新的部署完成（应该会自动开始）

### 步骤2：检查部署日志

部署完成后：

1. 点击最新的部署
2. 查看 "Build Logs" - 检查是否有构建错误
3. 查看 "Function Logs" - 这是最重要的，可以看到运行时错误

### 步骤3：测试端点

部署成功后，按以下顺序测试：

#### 3.1 测试根路径
```bash
curl https://my-space-beryl.vercel.app/
```

预期返回：
```json
{
  "message": "AI Resume Analyzer API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": ["/api/upload-resume", "/api/match-job"]
}
```

#### 3.2 测试健康检查
```bash
curl https://my-space-beryl.vercel.app/api/health
```

预期返回：
```json
{
  "status": "healthy",
  "openai_configured": true,
  "openai_model": "gpt-3.5-turbo",
  "openai_base_url": "https://api.openai-proxy.org/v1"
}
```

如果 `openai_configured` 为 `false`，说明环境变量没有正确配置。

#### 3.3 测试环境变量（使用test.py）
```bash
curl https://my-space-beryl.vercel.app/api/test
```

预期返回：
```json
{
  "status": "ok",
  "OPENAI_API_KEY": "exists",
  "OPENAI_API_KEY_length": 48,
  "OPENAI_API_KEY_preview": "sk-R4Z3s07...",
  "OPENAI_MODEL": "gpt-3.5-turbo",
  "OPENAI_BASE_URL": "https://api.openai-proxy.org/v1",
  "env_count": 10
}
```

### 步骤4：如果仍然出现500错误

1. 在Vercel Dashboard中查看 "Function Logs"
2. 查找包含 "ERROR" 或 "Traceback" 的日志
3. 将完整的错误日志发送给我

### 步骤5：如果出现404错误

404错误通常意味着：
- 路由配置问题
- 函数没有正确部署

检查：
1. 确认 `vercel.json` 文件在项目根目录
2. 确认 `api/index.py` 文件存在
3. 在Vercel Dashboard的 "Functions" 标签页查看是否有函数被部署

### 步骤6：环境变量确认

在Vercel Dashboard中：
1. 进入项目设置 (Settings)
2. 点击 "Environment Variables"
3. 确认以下变量存在且值正确：
   - `OPENAI_API_KEY`: `sk-R4Z3s07Fvg0nuvLlLtmMNe7EGRhv8DLhmlicxy9x6tEPRd7m`
   - `OPENAI_MODEL`: `gpt-3.5-turbo`
   - `OPENAI_BASE_URL`: `https://api.openai-proxy.org/v1`
4. 确认这些变量应用到了 "Production" 环境

## 常见问题排查

### 问题1：Import Error
**症状**：日志显示 "ModuleNotFoundError" 或 "ImportError"

**解决方案**：
- 检查 `api/requirements.txt` 是否包含所有依赖
- 检查 `api/services/__init__.py` 和 `api/utils/__init__.py` 是否存在

### 问题2：OpenAI API Error
**症状**：日志显示 "OpenAI API error" 或 "Authentication failed"

**解决方案**：
- 确认环境变量 `OPENAI_API_KEY` 正确设置
- 测试API key是否有效：
```bash
curl https://api.openai-proxy.org/v1/models \
  -H "Authorization: Bearer sk-R4Z3s07Fvg0nuvLlLtmMNe7EGRhv8DLhmlicxy9x6tEPRd7m"
```

### 问题3：Timeout Error
**症状**：请求超时或返回504

**解决方案**：
- Vercel免费版函数执行时间限制为10秒
- 如果AI处理时间过长，考虑：
  - 减少PDF文本长度
  - 降低 `MAX_TOKENS` 值
  - 使用更快的模型

### 问题4：Memory Error
**症状**：日志显示 "Out of memory" 或函数崩溃

**解决方案**：
- Vercel免费版内存限制为1024MB
- 优化PDF解析，避免加载过大的文件
- 在 `vercel.json` 中已设置 `maxLambdaSize: "50mb"`

## 调试技巧

### 查看实时日志
在Vercel Dashboard中：
1. 进入项目
2. 点击 "Logs" 标签
3. 选择 "Real-time" 查看实时日志
4. 发送请求到API，观察日志输出

### 使用浏览器开发者工具
1. 打开浏览器开发者工具 (F12)
2. 访问 https://my-space-beryl.vercel.app/
3. 查看 "Network" 标签
4. 查看请求的响应状态和内容

## 需要提供的信息

如果问题仍未解决，请提供：
1. Vercel部署的完整日志（Build Logs + Function Logs）
2. 访问API时的完整错误响应
3. 浏览器开发者工具中的Network请求详情
4. 环境变量配置截图（隐藏敏感信息）

## 联系支持

如果以上步骤都无法解决问题：
- Vercel支持：https://vercel.com/support
- OpenAI支持：https://help.openai.com/
