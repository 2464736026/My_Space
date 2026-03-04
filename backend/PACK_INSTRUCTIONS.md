# 阿里云函数计算部署完整指南

> 详细的打包和部署步骤

---

## 📦 第一步：准备代码包

### 1. 创建部署目录结构

确保你的 `backend` 目录包含以下文件：

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py
│   │   └── pdf_parser.py
│   └── utils/
│       ├── __init__.py
│       └── cache.py
├── index.py          ← 入口文件（重要！）
├── config.py
└── requirements.txt
```

### 2. 打包命令（Windows PowerShell）

```powershell
# 进入backend目录
cd E:\newP\backend

# 删除旧的压缩包（如果存在）
Remove-Item resume-analyzer.zip -ErrorAction SilentlyContinue

# 打包（只包含必要文件）
Compress-Archive -Path app,index.py,config.py,requirements.txt -DestinationPath resume-analyzer.zip -Force

# 验证压缩包
Write-Host "压缩包已创建：resume-analyzer.zip"
Get-Item resume-analyzer.zip | Select-Object Name, Length
```

### 3. 打包命令（Windows CMD）

```cmd
cd E:\newP\backend
del resume-analyzer.zip
powershell Compress-Archive -Path app,index.py,config.py,requirements.txt -DestinationPath resume-analyzer.zip -Force
```

---

## ☁️ 第二步：上传到阿里云

### 方法A：使用控制台上传代码包（推荐）

1. **登录阿里云函数计算控制台**
   - 访问：https://fcnext.console.aliyun.com/cn-hangzhou/functions
   - 选择你的函数（例如：`api`）

2. **上传代码包**
   - 点击"代码"标签
   - 点击"上传代码" → "上传 ZIP 包"
   - 选择 `resume-analyzer.zip`
   - 等待上传完成

3. **点击"部署"按钮**
   - 上传后必须点击"部署"才能生效
   - 等待部署完成（约10-30秒）

### 方法B：在线编辑代码（适合小改动）

1. **进入代码编辑器**
   - 在函数详情页点击"代码"标签
   - 可以直接在线编辑文件

2. **确保 index.py 完整**
   - 检查 `index.py` 文件是否完整
   - 应该有约98行代码
   - 包含完整的 `handler` 函数

3. **保存并部署**
   - 点击"保存"
   - 点击"部署"

---

## ⚙️ 第三步：配置函数

### 1. 基本配置

在函数配置页面设置：

- **函数名称**：`api`
- **运行环境**：`Python 3.10` 或 `Python 3.9`
- **函数入口**：`index.handler`（重要！）
- **内存规格**：`1024 MB`（推荐）或 `512 MB`（最低）
- **超时时间**：`60 秒`

### 2. 环境变量配置

在"环境变量"部分添加：

| 变量名 | 变量值 |
|--------|--------|
| `OPENAI_API_KEY` | `sk-R4Z3s07Fvg0nuvLlLtmMNe7EGRhv8DLhmlicxy9x6tEPRd7m` |
| `OPENAI_MODEL` | `gpt-3.5-turbo` |
| `OPENAI_BASE_URL` | `https://api.openai-proxy.org/v1` |

**重要**：环境变量配置后需要点击"保存"并重新"部署"！

### 3. HTTP触发器配置

确保HTTP触发器配置正确：

- **触发器类型**：HTTP触发器
- **触发器名称**：`httpTrigger`
- **请求方式**：全选（GET, POST, PUT, DELETE, OPTIONS）
- **鉴权方式**：`anonymous`（匿名访问）

---

## 🧪 第四步：测试部署

### 1. 获取函数URL

在"触发器"标签中，复制"公网访问地址"，例如：
```
https://1234567890.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/resume-analyzer/api/
```

### 2. 测试健康检查

在浏览器中访问：
```
https://你的FC地址/
```

**预期结果**：
```json
{
  "message": "AI Resume Analyzer API",
  "version": "1.0.0"
}
```

### 3. 测试API文档

访问：
```
https://你的FC地址/docs
```

应该能看到 Swagger API 文档界面。

### 4. 查看函数日志

如果出现错误：
1. 在函数详情页点击"日志查询"
2. 查看最近的调用日志
3. 找到错误信息

---

## ❌ 常见错误及解决方案

### 错误1：`required HTTP header Date was not specified`

**原因**：`index.py` 文件不完整或格式错误

**解决**：
1. 确保 `index.py` 包含完整的 `handler` 函数
2. 重新上传代码包
3. 或使用在线编辑器复制完整代码

### 错误2：`Request failed with status code 400`

**原因**：函数入口配置错误

**解决**：
1. 检查"函数入口"是否为 `index.handler`
2. 确保 `index.py` 文件在根目录
3. 重新部署

### 错误3：`Module not found: app.main`

**原因**：目录结构不正确或缺少文件

**解决**：
1. 确保 `app` 目录存在
2. 确保 `app/main.py` 存在
3. 确保所有 `__init__.py` 文件存在
4. 重新打包上传

### 错误4：`Internal Server Error (500)`

**原因**：代码运行时错误

**解决**：
1. 查看函数日志获取详细错误
2. 检查环境变量是否配置正确
3. 检查依赖是否完整

### 错误5：超时错误

**原因**：函数执行时间超过配置的超时时间

**解决**：
1. 增加超时时间到 60 秒
2. 增加内存到 1024 MB
3. 优化代码性能

---

## 📋 部署检查清单

完成部署前，请确认：

- [ ] 代码包已正确打包（包含 app, index.py, config.py, requirements.txt）
- [ ] 代码包已上传到阿里云
- [ ] 点击了"部署"按钮
- [ ] 函数入口设置为 `index.handler`
- [ ] 运行环境选择 Python 3.9 或 3.10
- [ ] 内存设置为 512MB 或更高
- [ ] 超时时间设置为 60 秒
- [ ] 环境变量已配置（OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL）
- [ ] HTTP触发器已创建
- [ ] 触发器鉴权方式设置为 anonymous
- [ ] 测试访问根路径返回正确的JSON
- [ ] 测试访问 /docs 能看到API文档

---

## 🎯 下一步

部署成功后：

1. **复制函数URL**
   ```
   https://你的FC地址/
   ```

2. **更新前端配置**
   - 编辑 `frontend/src/App.jsx`
   - 将 `API_BASE_URL` 更新为你的FC地址

3. **提交代码到GitHub**
   ```bash
   git add .
   git commit -m "Update: configure Aliyun FC API URL"
   git push origin main
   ```

4. **部署前端到GitHub Pages**
   - 在GitHub仓库设置中启用GitHub Pages
   - 选择部署分支

---

## 💡 提示

1. **每次修改代码后都要点击"部署"**
2. **环境变量修改后也要重新部署**
3. **查看日志是排查问题的最佳方式**
4. **测试时使用浏览器的开发者工具查看网络请求**

---

**现在开始部署吧！** 🚀
