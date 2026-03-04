# 🚀 Vercel 部署步骤 (5分钟完成)

## 准备工作 ✅

已完成的清理工作:
- ✅ 删除所有阿里云相关文件 (index.py, s.yaml, template.yml, 部署脚本等)
- ✅ 删除阿里云相关文档 (HOW_TO_SUBMIT.md, SUBMISSION_*.md, NEXT_STEPS.md 等)
- ✅ 创建 Vercel 配置文件 (vercel.json, api/index.py)
- ✅ 更新 .gitignore (忽略 backend/python/ 目录)
- ✅ 更新 README.md (添加 Vercel 部署说明)

---

## 第一步: 推送代码到 GitHub

```bash
# 查看当前状态
git status

# 添加所有更改
git add .

# 提交更改
git commit -m "Switch to Vercel deployment"

# 推送到 GitHub
git push origin main
```

**注意**: 如果推送失败,请确保:
- 已开启 VPN (访问 GitHub)
- 已配置 Git 用户信息
- 有仓库的推送权限

---

## 第二步: 在 Vercel 部署

### 2.1 注册/登录 Vercel

1. 访问: https://vercel.com
2. 点击 "Sign Up" 或 "Log In"
3. 选择 "Continue with GitHub"
4. 授权 Vercel 访问你的 GitHub

### 2.2 导入项目

1. 在 Vercel 控制台点击 "Add New..." → "Project"
2. 在列表中找到仓库: `My_Space`
3. 点击 "Import"

### 2.3 配置项目

**Framework Preset**: Other (保持默认)

**Root Directory**: `./` (保持默认)

**Build Command**: 留空

**Output Directory**: 留空

### 2.4 配置环境变量 (重要!)

点击 "Environment Variables",添加以下 3 个变量:

| Name | Value |
|------|-------|
| `OPENAI_API_KEY` | `sk-R4Z3s07Fvg0nuvLlLtmMNe7EGRhv8DLhmlicxy9x6tEPRd7m` |
| `OPENAI_MODEL` | `gpt-3.5-turbo` |
| `OPENAI_BASE_URL` | `https://api.openai-proxy.org/v1` |

**注意**: 
- 每个变量都要单独添加
- 确保变量名和值都正确无误
- 不要有多余的空格

### 2.5 开始部署

1. 点击 "Deploy" 按钮
2. 等待 2-3 分钟 (Vercel 会自动安装依赖并部署)
3. 部署成功后会显示你的网站地址

例如: `https://my-space-xxx.vercel.app`

---

## 第三步: 测试 API

### 3.1 测试根路径

访问: `https://your-project-name.vercel.app/`

应该看到:
```json
{
  "message": "AI Resume Analyzer API",
  "version": "1.0.0"
}
```

### 3.2 测试 API 文档

访问: `https://your-project-name.vercel.app/docs`

应该看到 FastAPI 自动生成的 API 文档界面

### 3.3 测试上传接口

在 API 文档页面测试 `/api/upload-resume` 接口

---

## 第四步: 更新前端配置

### 4.1 编辑前端代码

打开 `frontend/src/App.jsx`,找到第 47-50 行:

```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://your-project-name.vercel.app'  // 👈 替换这里
  : 'http://localhost:8000';
```

将 `your-project-name` 替换为你的实际 Vercel 域名

例如:
```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://my-space-abc123.vercel.app'
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

## 第五步: 验证部署

### 5.1 等待自动部署完成

在 Vercel 控制台查看部署状态:
1. 点击你的项目
2. 查看 "Deployments" 标签
3. 等待最新的部署变为 "Ready"

### 5.2 完整测试流程

1. 访问你的 Vercel 地址
2. 填写岗位需求
3. 上传测试 PDF 简历
4. 查看分析结果

---

## 🎉 完成!

你的 AI 简历分析系统已成功部署到 Vercel!

**后端 API**: `https://your-project-name.vercel.app`

**API 文档**: `https://your-project-name.vercel.app/docs`

---

## 📊 部署检查清单

- [ ] 代码已推送到 GitHub
- [ ] 在 Vercel 导入项目
- [ ] 配置 3 个环境变量 (OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL)
- [ ] 首次部署成功
- [ ] 测试根路径 (/)
- [ ] 测试 API 文档 (/docs)
- [ ] 更新前端 API 地址
- [ ] 重新部署成功
- [ ] 完整功能测试通过

---

## 🔧 常见问题

### Q1: 部署失败 - ModuleNotFoundError

**原因**: 缺少依赖包

**解决**: 
1. 检查 `backend/requirements.txt` 是否包含所有依赖
2. 确保包含 `mangum==0.17.0`
3. 在 Vercel 控制台查看详细错误日志

### Q2: 部署失败 - Environment Variable Missing

**原因**: 环境变量未配置或配置错误

**解决**:
1. 在 Vercel 项目设置中检查环境变量
2. 确保 3 个变量都已添加
3. 检查变量名是否正确 (区分大小写)
4. 重新部署

### Q3: API 返回 500 错误

**原因**: OpenAI API 调用失败

**解决**:
1. 在 Vercel 控制台查看 "Logs"
2. 检查 OPENAI_API_KEY 是否正确
3. 检查 OPENAI_BASE_URL 是否可访问
4. 测试 API Key 是否有效

### Q4: 前端无法连接后端

**原因**: API 地址配置错误

**解决**:
1. 检查 `frontend/src/App.jsx` 中的 API_BASE_URL
2. 确保使用正确的 Vercel 域名
3. 检查浏览器控制台的网络请求
4. 确认后端 API 正常运行

### Q5: 如何查看日志?

1. 在 Vercel 控制台点击项目
2. 点击 "Logs" 标签
3. 选择时间范围
4. 查看实时日志和错误信息

### Q6: 如何重新部署?

**方法1**: 推送代码自动部署
```bash
git add .
git commit -m "Update"
git push origin main
```

**方法2**: 手动触发部署
1. 在 Vercel 控制台点击项目
2. 点击 "Deployments"
3. 点击最新部署右侧的 "..." 菜单
4. 选择 "Redeploy"

---

## 💡 提示

1. **自动部署**: 每次推送到 GitHub 都会自动触发 Vercel 部署
2. **环境变量**: 修改环境变量后需要手动重新部署
3. **日志查看**: 遇到问题先查看 Vercel 的日志
4. **域名绑定**: 可以在 Vercel 设置中绑定自定义域名
5. **免费额度**: Vercel 个人项目完全免费,无需担心费用

---

## 📚 相关资源

- Vercel 官方文档: https://vercel.com/docs
- FastAPI 文档: https://fastapi.tiangolo.com
- Mangum 文档: https://mangum.io
- GitHub 仓库: https://github.com/2464736026/My_Space

---

**现在就开始部署吧!** 🚀
