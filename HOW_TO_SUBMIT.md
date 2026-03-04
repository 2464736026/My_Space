# 如何提交项目 - 快速指南

> 5步完成项目提交和部署

---

## 📋 准备工作

确保你已经：
- ✅ 完成所有功能开发
- ✅ 在 `backend/config.py` 中配置了OpenAI API密钥
- ✅ 本地测试通过

---

## 🚀 提交步骤

### 步骤1：创建GitHub仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - Repository name: `ai-resume-analyzer`
   - Description: `AI智能简历分析系统 - 基于OpenAI GPT的简历筛选与岗位匹配`
   - 选择 **Public**（公开）
3. 不要勾选任何初始化选项
4. 点击 **Create repository**

### 步骤2：推送代码到GitHub

```bash
# 初始化Git仓库（如果还没有）
git init

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/ai-resume-analyzer.git

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: AI Resume Analyzer"

# 推送到GitHub
git push -u origin main
```

如果推送失败，可能需要先创建main分支：
```bash
git branch -M main
git push -u origin main
```

### 步骤3：部署后端到阿里云函数计算

#### 3.1 安装Funcraft工具

```bash
# 使用npm安装
npm install @alicloud/fun -g

# 验证安装
fun --version
```

#### 3.2 配置阿里云账号

```bash
fun config
```

按提示输入：
- **Account ID**: 在阿里云控制台右上角查看
- **Access Key ID**: 访问 https://ram.console.aliyun.com/manage/ak 创建
- **Access Key Secret**: 创建AccessKey时获得
- **Default Region**: 选择 `cn-hangzhou` 或其他区域

#### 3.3 部署函数

```bash
# 进入后端目录
cd backend

# 部署
fun deploy

# 部署成功后会显示HTTP触发器地址，例如：
# https://1234567890.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/resume-analyzer/api/
```

**重要**：复制这个地址，后面会用到！

#### 3.4 配置CORS

1. 登录阿里云函数计算控制台
2. 找到你的函数：`resume-analyzer/api`
3. 点击 **配置** → **触发器**
4. 编辑HTTP触发器，添加CORS配置：
   ```
   允许的源: *
   允许的方法: GET, POST, PUT, DELETE, OPTIONS
   允许的头: *
   ```

### 步骤4：更新前端API地址并部署

#### 4.1 更新API地址

编辑 `frontend/src/App.jsx`，找到这一行：

```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://your-fc-domain.com' 
  : 'http://localhost:8000';
```

替换为你的阿里云FC地址：

```javascript
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://1234567890.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/resume-analyzer/api' 
  : 'http://localhost:8000';
```

#### 4.2 提交更改

```bash
git add frontend/src/App.jsx
git commit -m "Update: configure production API URL"
git push origin main
```

#### 4.3 启用GitHub Pages

1. 进入GitHub仓库页面
2. 点击 **Settings** → **Pages**
3. Source选择：`gh-pages` 分支
4. 点击 **Save**

#### 4.4 等待自动部署

- GitHub Actions会自动构建并部署前端
- 访问 `https://github.com/你的用户名/ai-resume-analyzer/actions` 查看进度
- 通常需要1-2分钟

### 步骤5：测试和提交

#### 5.1 测试在线演示

访问你的GitHub Pages地址：
```
https://你的用户名.github.io/resume-analyzer/
```

测试功能：
1. 填写岗位需求
2. 上传测试PDF简历
3. 查看分析结果
4. 测试PDF预览

#### 5.2 准备提交材料

填写以下信息：

**GitHub仓库地址**：
```
https://github.com/你的用户名/ai-resume-analyzer
```

**在线演示地址**：
```
前端: https://你的用户名.github.io/resume-analyzer/
后端: https://你的FC地址.cn-hangzhou.fc.aliyuncs.com/...
API文档: https://你的FC地址.cn-hangzhou.fc.aliyuncs.com/docs
```

**项目说明**：
```
AI智能简历分析系统 - 基于OpenAI GPT的智能简历筛选与岗位匹配系统

技术栈：
- 后端：Python + FastAPI + OpenAI GPT-3.5-turbo
- 前端：React + Vite + Ant Design
- 部署：阿里云函数计算 + GitHub Pages

核心功能：
✅ PDF简历上传与解析（支持多页）
✅ AI智能信息提取（基本信息、求职信息、背景信息）
✅ 三维智能评分（技能50% + 经验30% + 职位20%）
✅ 批量处理与自动排序
✅ PDF在线预览
✅ 缓存机制

项目亮点：
1. 完全AI驱动，摆脱传统规则提取
2. 支持批量上传，智能排序
3. 现代化UI设计，用户体验优秀
4. Serverless架构，弹性伸缩
5. 完整文档，易于维护
```

---

## 🎯 快速命令参考

### Git命令

```bash
# 初始化并推送
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/ai-resume-analyzer.git
git push -u origin main

# 更新代码
git add .
git commit -m "Update: your message"
git push origin main
```

### 阿里云FC部署

```bash
# 安装工具
npm install @alicloud/fun -g

# 配置账号
fun config

# 部署
cd backend
fun deploy
```

### 本地测试

```bash
# 启动开发服务
python start_dev.py

# 或手动启动
cd backend && uvicorn app.main:app --reload
cd frontend && npm run dev
```

---

## ❓ 常见问题

### Q1: GitHub推送失败

**错误**: `Permission denied (publickey)`

**解决**：
```bash
# 使用HTTPS而不是SSH
git remote set-url origin https://github.com/你的用户名/ai-resume-analyzer.git
```

### Q2: Funcraft部署失败

**错误**: `AccessDenied`

**解决**：
1. 确认AccessKey有足够权限
2. 在RAM控制台给用户添加 `AliyunFCFullAccess` 权限

### Q3: GitHub Pages显示404

**解决**：
1. 确认GitHub Actions构建成功
2. 确认Pages设置选择了 `gh-pages` 分支
3. 等待5-10分钟让DNS生效

### Q4: 前端无法连接后端

**解决**：
1. 确认 `App.jsx` 中的API地址正确
2. 确认阿里云FC的CORS已配置
3. 在浏览器控制台查看具体错误

---

## 📞 需要帮助？

查看详细文档：
- `README.md` - 项目完整说明
- `DEPLOYMENT_GUIDE.md` - 详细部署指南
- `TECHNICAL_INTERVIEW_GUIDE.md` - 技术面试准备
- `SUBMISSION_CHECKLIST.md` - 提交检查清单

---

## ✅ 提交检查清单

提交前确认：
- [ ] GitHub仓库已创建且为公开
- [ ] 代码已推送到main分支
- [ ] 后端已部署到阿里云FC
- [ ] 前端已部署到GitHub Pages
- [ ] 在线演示可正常访问
- [ ] 所有功能测试通过
- [ ] 文档完整

---

## 🎉 完成！

恭喜你完成了项目的提交和部署！

现在你可以：
1. 将GitHub仓库地址和在线演示地址提交给评审团队
2. 准备技术面试（参考 `TECHNICAL_INTERVIEW_GUIDE.md`）
3. 等待反馈并持续优化

**祝你成功！** 🚀
