# Vercel 部署指南 - AI简历分析系统

## 📋 准备工作

确保你已经:
- ✅ 有 GitHub 账号
- ✅ 代码已推送到 GitHub 仓库: `https://github.com/2464736026/My_Space`
- ✅ 有 VPN 访问 GitHub (如需要)

---

## 🚀 第一步: 推送代码到 GitHub

```bash
# 添加所有更改
git add .

# 提交更改
git commit -m "Prepare for Vercel deployment"

# 推送到 GitHub
git push origin main
```

---

## 🌐 第二步: 部署到 Vercel

### 2.1 注册 Vercel

1. 访问: https://vercel.com
2. 点击 "Sign Up"
3. 选择 "Continue with GitHub"
4. 授权 Vercel 访问你的 GitHub

### 2.2 导入项目

1. 在 Vercel 控制台点击 "Add New..." → "Project"
2. 找到并选择仓库: `My_Space`
3. 点击 "Import"

### 2.3 配置项目

**Framework Preset**: Other (保持默认)

**Root Directory**: `./` (保持默认)

**Environment Variables** (重要!):

点击 "Environment Variables" 添加以下三个变量:

| Name | Value |
|------|-------|
| `OPENAI_API_KEY` | `sk-R4Z3s07Fvg0nuvLlLtmMNe7EGRhv8DLhmlicxy9x6tEPRd7m` |
| `OPENAI_MODEL` | `gpt-3.5-turbo` |
| `OPENAI_BASE_URL` | `https://api.openai-proxy.org/v1` |

### 2.4 部署

1. 点击 "Deploy" 按钮
2. 等待 2-3 分钟
3. 部署成功后会显示你的网站地址

例如: `https://my-space-xxx.vercel.app`

---

## ✅ 第三步: 测试 API

部署成功后,访问你的 Vercel 地址:

```
https://your-project-name.vercel.app/
```

应该看到:
```json
{
  "message": "AI Resume Analyzer API",
  "version": "1.0.0"
}
```

测试上传接口:
```
https://your-project-name.vercel.app/api/upload-resume
```

---

## 🔧 第四步: 更新前端配置

部署成功后,需要更新前端的 API 地址:

### 4.1 编辑 `frontend/src/App.jsx`

找到第 47-50 行,将 `your-project-name` 替换为你的实际 Vercel 域名:

```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://my-space-xxx.vercel.app'  // 替换为你的实际域名
  : 'http://localhost:8000';
```

### 4.2 提交并推送

```bash
git add frontend/src/App.jsx
git commit -m "Update: configure Vercel API URL"
git push origin main
```

Vercel 会自动检测到更新并重新部署!

---

## 📱 第五步: 部署前端 (可选)

如果你想将前端也部署到 Vercel:

### 方法1: 使用 Vercel 部署前端

1. 在 Vercel 控制台再次点击 "Add New..." → "Project"
2. 选择同一个仓库 `My_Space`
3. 配置:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. 点击 "Deploy"

### 方法2: 使用 GitHub Pages

```bash
cd frontend
npm run build

# 将 dist 目录部署到 GitHub Pages
# (需要配置 GitHub Pages 设置)
```

---

## 🎯 完整的项目结构

```
My_Space/
├── api/
│   └── index.py          # Vercel 入口文件 (Mangum)
├── backend/
│   ├── app/
│   │   ├── main.py       # FastAPI 应用
│   │   ├── services/     # AI 和 PDF 服务
│   │   └── utils/        # 工具函数
│   ├── config.py         # 配置文件 (不提交到 Git)
│   └── requirements.txt  # Python 依赖
├── frontend/
│   └── src/
│       └── App.jsx       # React 前端
├── vercel.json           # Vercel 配置
└── .gitignore            # Git 忽略文件
```

---

## 🔍 常见问题

### Q1: 部署失败怎么办?

1. 在 Vercel 控制台点击项目
2. 点击 "Deployments"
3. 点击失败的部署查看日志
4. 检查错误信息

常见错误:
- **ModuleNotFoundError**: 检查 `requirements.txt` 是否包含所有依赖
- **Environment Variable Missing**: 检查环境变量是否正确配置

### Q2: API 返回 500 错误?

1. 在 Vercel 控制台点击 "Logs"
2. 查看实时日志
3. 检查 OpenAI API Key 是否正确
4. 检查 `OPENAI_BASE_URL` 是否可访问

### Q3: 如何更新代码?

只需推送到 GitHub:
```bash
git add .
git commit -m "Update code"
git push origin main
```

Vercel 会自动检测并重新部署!

### Q4: 如何查看日志?

1. 在 Vercel 控制台点击项目
2. 点击 "Logs"
3. 选择时间范围查看实时日志

---

## ✨ Vercel 的优势

1. **自动部署** - 推送到 GitHub 自动部署
2. **跨平台兼容** - 无需担心 Windows/Linux 差异
3. **免费额度** - 个人项目完全免费
4. **全球 CDN** - 访问速度快
5. **简单配置** - 无需配置服务器

---

## 📊 部署检查清单

- [ ] 代码已推送到 GitHub
- [ ] 在 Vercel 导入项目
- [ ] 配置环境变量 (OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL)
- [ ] 部署成功
- [ ] 测试 API 根路径
- [ ] 测试上传接口
- [ ] 更新前端 API 地址
- [ ] 重新部署前端

---

## 🎉 完成!

现在你的 AI 简历分析系统已经成功部署到 Vercel!

**后端 API**: `https://your-project-name.vercel.app`

**API 文档**: `https://your-project-name.vercel.app/docs`

---

## 📞 需要帮助?

- Vercel 文档: https://vercel.com/docs
- FastAPI 文档: https://fastapi.tiangolo.com
- GitHub 仓库: https://github.com/2464736026/My_Space
