# 部署指南 - AI智能简历分析系统

> 完整的云端部署流程：阿里云函数计算 + GitHub Pages

---

## 📋 部署清单

### ✅ 已完成的功能模块

- [x] **模块一：简历上传与解析** - 支持PDF上传、多页解析、文本清洗
- [x] **模块二：关键信息提取** - AI提取基本信息、求职信息、背景信息
- [x] **模块三：简历评分与匹配** - AI智能评分、三维匹配算法
- [x] **模块四：结果返回与缓存** - JSON格式返回、内存缓存机制
- [x] **模块五：前端页面** - React + Ant Design，响应式设计

---

## 🚀 部署流程

### 第一步：准备工作

#### 1.1 确认项目完整性

```bash
# 检查项目结构
ls -la

# 应该包含以下文件/目录：
# ├── backend/          # 后端代码
# ├── frontend/         # 前端代码
# ├── .github/          # GitHub Actions配置
# ├── README.md         # 项目文档
# └── DEPLOYMENT_GUIDE.md  # 本文件
```

#### 1.2 确认API密钥配置

编辑 `backend/config.py`，确保已填写有效的OpenAI API密钥：

```python
OPENAI_API_KEY = "sk-your-actual-api-key-here"  # 必须填写
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_BASE_URL = "https://api.openai-proxy.org/v1"  # 如使用代理
```

---

### 第二步：部署后端到阿里云函数计算（FC）

#### 2.1 安装阿里云CLI工具

```bash
# 方式一：使用pip安装
pip install aliyun-fc2

# 方式二：下载Funcraft工具
npm install @alicloud/fun -g
```

#### 2.2 配置阿里云账号

```bash
# 配置访问凭证
fun config

# 按提示输入：
# - Account ID: 你的阿里云账号ID
# - Access Key ID: 访问密钥ID
# - Access Key Secret: 访问密钥Secret
# - Default Region: cn-hangzhou（或其他区域）
```

获取访问密钥：
1. 登录阿里云控制台
2. 访问：https://ram.console.aliyun.com/manage/ak
3. 创建AccessKey并保存

#### 2.3 准备部署文件

确保 `backend/template.yml` 配置正确：

```yaml
ROSTemplateFormatVersion: '2015-09-01'
Transform: 'Aliyun::Serverless-2018-04-03'
Resources:
  resume-analyzer:
    Type: 'Aliyun::Serverless::Service'
    Properties:
      Description: 'AI Resume Analyzer Service'
    api:
      Type: 'Aliyun::Serverless::Function'
      Properties:
        Description: 'Resume analyzer API'
        CodeUri: './'
        Handler: app.main:app
        Runtime: python3.9
        Timeout: 60
        MemorySize: 512
        EnvironmentVariables:
          OPENAI_API_KEY: 'your-openai-api-key-here'  # 替换为实际密钥
          OPENAI_MODEL: 'gpt-3.5-turbo'
          OPENAI_BASE_URL: 'https://api.openai-proxy.org/v1'
        Events:
          httpTrigger:
            Type: HTTP
            Properties:
              AuthType: ANONYMOUS
              Methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
```

#### 2.4 部署到函数计算

```bash
# 进入后端目录
cd backend

# 部署函数
fun deploy

# 部署成功后会显示函数的HTTP触发器地址，例如：
# https://1234567890.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/resume-analyzer/api/
```

#### 2.5 测试后端API

```bash
# 测试健康检查
curl https://your-fc-domain.com/

# 应该返回：
# {"message": "AI Resume Analyzer API", "version": "1.0.0"}
```

#### 2.6 配置CORS（重要）

在阿里云函数计算控制台：
1. 进入函数详情页
2. 配置 → HTTP触发器
3. 添加CORS配置：
   - 允许的源：`*` 或你的GitHub Pages域名
   - 允许的方法：`GET, POST, PUT, DELETE, OPTIONS`
   - 允许的头：`*`

---

### 第三步：部署前端到GitHub Pages

#### 3.1 创建GitHub仓库

```bash
# 初始化Git仓库（如果还没有）
git init

# 添加远程仓库
git remote add origin https://github.com/your-username/ai-resume-analyzer.git

# 提交代码
git add .
git commit -m "Initial commit: AI Resume Analyzer"
git push -u origin main
```

#### 3.2 配置前端API地址

编辑 `frontend/src/App.jsx`，更新API地址：

```javascript
// 修改这一行，替换为你的阿里云FC地址
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://your-fc-domain.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/resume-analyzer/api' 
  : 'http://localhost:8000';
```

#### 3.3 启用GitHub Pages

1. 进入GitHub仓库页面
2. 点击 `Settings` → `Pages`
3. Source选择：`gh-pages` 分支
4. 点击 `Save`

#### 3.4 自动部署

项目已配置GitHub Actions自动部署（`.github/workflows/deploy.yml`）：

```bash
# 每次推送到main分支时自动部署
git add .
git commit -m "Update: configure production API"
git push origin main

# 等待1-2分钟，GitHub Actions会自动构建并部署
```

#### 3.5 访问前端页面

部署成功后，访问：
```
https://your-username.github.io/resume-analyzer/
```

---

## 🔧 配置检查清单

### 后端配置

- [ ] `backend/config.py` - OpenAI API密钥已配置
- [ ] `backend/template.yml` - 环境变量已设置
- [ ] 阿里云FC已部署成功
- [ ] HTTP触发器可访问
- [ ] CORS已正确配置

### 前端配置

- [ ] `frontend/src/App.jsx` - API_BASE_URL已更新为FC地址
- [ ] `frontend/vite.config.js` - base路径正确（/resume-analyzer/）
- [ ] GitHub仓库已创建
- [ ] GitHub Pages已启用
- [ ] 前端页面可访问

---

## 📝 提交材料准备

### 1. 项目仓库地址

```
GitHub仓库：https://github.com/your-username/ai-resume-analyzer
```

### 2. 在线演示地址

```
前端页面：https://your-username.github.io/resume-analyzer/
后端API：https://your-fc-domain.cn-hangzhou.fc.aliyuncs.com/...
```

### 3. API文档地址

```
Swagger文档：https://your-fc-domain.com/docs
```

### 4. 项目说明文档

提交以下文档：
- `README.md` - 项目完整说明
- `TECHNICAL_INTERVIEW_GUIDE.md` - 技术面试指南
- `DEPLOYMENT_GUIDE.md` - 本部署指南

---

## 🧪 功能验证

### 验证步骤

1. **访问前端页面**
   - 打开 GitHub Pages 地址
   - 确认页面正常加载

2. **配置岗位需求**
   - 填写职位名称、经验要求、技能要求、职位描述
   - 点击"保存岗位需求"

3. **上传测试简历**
   - 使用项目中的 `test_resume_sample.txt` 转换为PDF
   - 或使用真实的PDF简历
   - 批量上传多份简历

4. **查看分析结果**
   - 确认AI成功提取信息
   - 确认评分和排序正确
   - 点击查看详情和PDF预览

5. **测试API接口**
   ```bash
   # 测试上传接口
   curl -X POST "https://your-fc-domain.com/api/upload-resume" \
     -F "file=@test_resume.pdf"
   
   # 测试匹配接口
   curl -X POST "https://your-fc-domain.com/api/match-job" \
     -H "Content-Type: application/json" \
     -d '{
       "resume_id": "xxx",
       "job_title": "Python工程师",
       "job_description": "...",
       "required_skills": "Python, FastAPI",
       "experience_level": "3-5年"
     }'
   ```

---

## 🎯 评分要点对照

### 必选功能（已完成）

| 功能模块 | 要求 | 实现状态 |
|---------|------|---------|
| 简历上传与解析 | 支持PDF上传、多页解析、文本清洗 | ✅ 完成 |
| 关键信息提取 | AI提取基本信息（姓名、电话、邮箱等） | ✅ 完成 |
| 简历评分与匹配 | 岗位匹配、评分计算 | ✅ 完成 |
| 结果返回 | JSON格式返回 | ✅ 完成 |
| 前端页面 | 可用的交互页面 | ✅ 完成 |
| 云端部署 | 阿里云FC + GitHub Pages | ✅ 配置完成 |

### 加分项（已完成）

| 加分项 | 实现状态 |
|-------|---------|
| 提取求职信息（求职意向、期望薪资） | ✅ 完成 |
| 提取背景信息（工作年限、学历、项目经历） | ✅ 完成 |
| AI模型精准评分 | ✅ 完成（OpenAI GPT） |
| 缓存机制 | ✅ 完成（内存缓存） |
| 批量上传 | ✅ 完成 |
| 智能排序 | ✅ 完成 |
| PDF预览 | ✅ 完成 |

---

## 💡 技术亮点说明

### 1. 完全AI驱动
- 使用OpenAI GPT-3.5-turbo/GPT-4
- 摆脱传统规则提取，适应各种简历格式
- 语义理解能力强，准确率高

### 2. 三维评分算法
```
综合评分 = 技能匹配度 × 50% + 经验匹配度 × 30% + 职位匹配度 × 20%
```

### 3. 批量处理与智能排序
- 支持同时上传多份简历
- 自动按AI评分排序
- 前三名特殊标识

### 4. 现代化架构
- 后端：Python + FastAPI（高性能异步）
- 前端：React + Vite + Ant Design
- 部署：Serverless架构（阿里云FC）

### 5. 用户体验优化
- PDF在线预览
- 详细分析报告
- 响应式设计
- 流畅动画效果

---

## 🐛 常见问题

### Q1: 阿里云FC部署失败

**解决方案**：
1. 检查 `template.yml` 配置是否正确
2. 确认阿里云账号权限充足
3. 查看函数计算控制台的错误日志
4. 确认依赖包大小不超过限制（建议使用层）

### Q2: GitHub Pages无法访问

**解决方案**：
1. 确认GitHub Actions构建成功（查看Actions标签页）
2. 确认Pages设置中选择了 `gh-pages` 分支
3. 等待5-10分钟让DNS生效
4. 检查浏览器控制台是否有CORS错误

### Q3: 前端无法连接后端

**解决方案**：
1. 确认 `App.jsx` 中的 `API_BASE_URL` 正确
2. 确认阿里云FC的CORS配置正确
3. 在浏览器控制台查看具体错误信息
4. 使用curl测试后端API是否可访问

### Q4: AI提取信息不准确

**解决方案**：
1. 尝试使用GPT-4模型（修改 `config.py`）
2. 优化提示词（在 `config.py` 中调整）
3. 确认PDF文件包含可提取的文本（非扫描件）

---

## 📞 提交前最终检查

### 代码提交

```bash
# 1. 确认所有更改已提交
git status

# 2. 提交最终版本
git add .
git commit -m "Final: Ready for deployment"
git push origin main

# 3. 创建发布标签
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 提交材料清单

- [ ] GitHub仓库地址（公开）
- [ ] 在线演示地址（前端 + 后端）
- [ ] README.md（项目说明）
- [ ] TECHNICAL_INTERVIEW_GUIDE.md（技术说明）
- [ ] DEPLOYMENT_GUIDE.md（部署说明）
- [ ] 测试视频或截图（可选）

---

## 🎉 完成！

恭喜你完成了AI智能简历分析系统的开发和部署！

**项目亮点总结**：
- ✅ 完全AI驱动，智能提取和评分
- ✅ 批量处理，自动排序
- ✅ 现代化UI，用户体验优秀
- ✅ Serverless架构，弹性伸缩
- ✅ 完整文档，易于维护

**下一步**：
1. 将GitHub仓库地址和在线演示地址提交给评审团队
2. 准备技术面试，参考 `TECHNICAL_INTERVIEW_GUIDE.md`
3. 根据反馈进行优化和改进

祝你面试成功！🚀
