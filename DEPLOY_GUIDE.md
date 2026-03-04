# 阿里云部署指南

## 第一步：打包代码

运行：
```cmd
cd backend
deploy_aliyun.bat
```

## 第二步：上传到阿里云

1. 访问：https://fcnext.console.aliyun.com/cn-hangzhou/functions
2. 选择你的函数
3. 点击"代码" → "上传 ZIP 包"
4. 选择 `resume-analyzer.zip`
5. **点击"部署"**

## 第三步：配置环境变量

在"配置"标签中添加：
```
OPENAI_API_KEY = sk-R4Z3s07Fvg0nuvLlLtmMNe7EGRhv8DLhmlicxy9x6tEPRd7m
OPENAI_MODEL = gpt-3.5-turbo
OPENAI_BASE_URL = https://api.openai-proxy.org/v1
```

点击"保存"并重新"部署"

## 第四步：确认配置

- 函数入口：`index.handler`
- 运行环境：`Python 3.10`
- 内存：`1024 MB`
- 超时：`60 秒`

## 测试

访问你的FC地址，应该看到：
```json
{"message": "AI Resume Analyzer API", "version": "1.0.0"}
```
