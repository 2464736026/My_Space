# AI智能简历分析系统

> 基于人工智能的简历解析与岗位匹配平台，支持批量分析，智能排序

[![部署状态](https://img.shields.io/badge/部署-成功-brightgreen)](https://my-space-frontend.vercel.app)
[![后端API](https://img.shields.io/badge/API-运行中-blue)](https://my-space-beryl.vercel.app)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

## 📋 项目简介

AI智能简历分析系统是一个全栈Web应用，利用OpenAI GPT模型自动解析PDF简历，提取关键信息，并根据岗位需求进行智能匹配评分。系统支持批量上传简历，自动按匹配度排序，为HR提供高效的候选人筛选工具。

### 核心功能

- 🤖 **AI智能解析**：自动提取简历中的姓名、联系方式、工作经验、技能等信息
- 📊 **岗位匹配评分**：基于技能、经验、职位三个维度进行智能评分（0-100分）
- 📁 **批量处理**：支持同时上传多份PDF简历，自动分析并排序
- 🏆 **智能排序**：按匹配度自动排序，金银铜牌标识，推荐面试建议
- 📄 **PDF预览**：在线查看原始简历，详情弹窗展示完整信息
- 💡 **AI建议**：提供候选人改进建议和面试评估

### 在线演示

- **前端应用**：https://my-space-frontend.vercel.app
- **后端API**：https://my-space-beryl.vercel.app
- **API文档**：https://my-space-beryl.vercel.app/api/health

## 🛠️ 技术栈

### 前端技术

- **框架**：React 18.2.0
- **构建工具**：Vite 5.0.8
- **UI组件库**：Ant Design 5.12.2
- **HTTP客户端**：Axios 1.6.2
- **图标库**：@ant-design/icons 5.2.6
- **部署平台**：Vercel

### 后端技术

- **运行时**：Python 3.12
- **Web框架**：Vercel原生Python Handler（BaseHTTPRequestHandler）
- **PDF解析**：pdfplumber 0.10.3, PyPDF2 3.0.1
- **AI服务**：OpenAI GPT-3.5-turbo（通过HTTP直接调用）
- **图像处理**：Pillow 10.2.0
- **文本提取**：pdfminer.six 20221105
- **部署平台**：Vercel Serverless Functions

### 开发工具

- **版本控制**：Git & GitHub
- **包管理**：npm (前端), pip (后端)
- **代码编辑器**：VS Code
- **API测试**：Postman / curl

## 📁 项目结构

```
My_Space/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── App.jsx          # 主应用组件
│   │   ├── index.css        # 全局样式
│   │   └── main.jsx         # 入口文件
│   ├── public/              # 静态资源
│   ├── package.json         # 前端依赖
│   ├── vite.config.js       # Vite配置
│   └── vercel.json          # Vercel前端配置
│
├── api/                      # 后端API
│   ├── services/
│   │   ├── ai_service.py    # AI服务（OpenAI API调用）
│   │   ├── pdf_parser.py    # PDF解析服务
│   │   └── __init__.py
│   ├── utils/
│   │   ├── cache.py         # 缓存管理
│   │   └── __init__.py
│   ├── index.py             # API主入口（Vercel Handler）
│   ├── config.py            # 配置文件
│   └── requirements.txt     # Python依赖
│
├── vercel.json              # Vercel后端配置
├── requirements.txt         # 根目录依赖
├── README.md                # 项目说明（本文件）
└── 技术实现文档.md          # 详细技术文档

```

## 🚀 快速开始

### 前置要求

- Node.js >= 18.0.0
- Python >= 3.12
- Git
- Vercel账号（用于部署）

### 本地开发

#### 1. 克隆项目

```bash
git clone https://github.com/2464736026/My_Space.git
cd My_Space
```

#### 2. 配置环境变量

创建 `.env` 文件：

```env
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_BASE_URL=https://api.openai-proxy.org/v1
```

#### 3. 启动后端

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

后端将运行在 http://localhost:8000

#### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端将运行在 http://localhost:5173

### 部署到Vercel

#### 后端部署

1. 在Vercel Dashboard中导入GitHub仓库
2. 项目名称：`my-space`
3. Root Directory：留空（使用根目录）
4. Framework Preset：Other
5. 配置环境变量：
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL`
   - `OPENAI_BASE_URL`
6. 点击Deploy

#### 前端部署

1. 再次导入同一个GitHub仓库
2. 项目名称：`my-space-frontend`
3. Root Directory：`frontend`
4. Framework Preset：Vite
5. 点击Deploy

## 📖 使用指南

### 1. 配置岗位需求

访问前端应用，填写招聘岗位信息：
- 职位名称（如：Python后端工程师）
- 经验要求（如：3-5年工作经验）
- 技能要求（如：Python, FastAPI, MySQL, Redis）
- 职位描述（详细描述岗位职责和要求）

### 2. 上传简历

- 支持拖拽上传或点击选择
- 支持批量上传多个PDF文件
- 文件大小限制：4MB以内
- 格式要求：文本型PDF（可复制文字）

### 3. 查看分析结果

系统自动：
- 解析简历内容
- 提取关键信息
- 计算匹配评分
- 按评分排序显示

### 4. 查看候选人详情

点击候选人卡片可查看：
- 基本信息（姓名、电话、邮箱）
- 工作经验和学历
- 技能列表和项目经验
- 匹配度详细分析
- AI评价和改进建议
- 原始PDF预览

## 🎯 核心功能实现

### AI简历解析

使用OpenAI GPT-3.5-turbo模型，通过精心设计的提示词（Prompt）提取简历信息：

```python
# 提取简历信息
extracted_info = ai_service.extract_resume_info(pdf_text)

# 返回结构化数据
{
    "basic_info": {
        "name": "张三",
        "phone": "13800138000",
        "email": "zhangsan@example.com"
    },
    "job_info": {
        "position": "Python工程师",
        "salary": "15-20K"
    },
    "background": {
        "work_years": "3年",
        "education": "本科",
        "skills": ["Python", "FastAPI", "MySQL"],
        "projects": ["电商平台", "用户系统"]
    }
}
```

### 岗位匹配评分

基于三个维度进行评分：

1. **技能匹配度**（50%权重）
   - 匹配技能列表
   - 缺失技能列表
   - 评分：0-100分

2. **经验匹配度**（30%权重）
   - 工作年限对比
   - 行业经验评估
   - 评分：0-100分

3. **职位匹配度**（20%权重）
   - 求职意向对比
   - 职业发展路径
   - 评分：0-100分

**综合评分** = 技能匹配 × 0.5 + 经验匹配 × 0.3 + 职位匹配 × 0.2

### 批量处理与排序

```javascript
// 批量上传处理
for (const file of fileList) {
  // 1. 上传PDF
  const uploadResponse = await axios.post('/api/upload-resume', formData);
  
  // 2. 岗位匹配
  const matchResponse = await axios.post('/api/match-job', {
    resume_id: uploadResponse.data.resume_id,
    ...jobRequirement
  });
  
  // 3. 添加到候选人列表
  candidates.push({
    ...uploadResponse.data,
    ...matchResponse.data
  });
}

// 按评分排序
candidates.sort((a, b) => b.matchResult.total_score - a.matchResult.total_score);
```

## 🔧 API接口

### 健康检查

```http
GET /api/health
```

**响应：**
```json
{
  "status": "healthy",
  "openai_configured": true,
  "openai_model": "gpt-3.5-turbo"
}
```

### 上传简历

```http
POST /api/upload-resume
Content-Type: multipart/form-data

file: <PDF文件>
```

**响应：**
```json
{
  "success": true,
  "data": {
    "resume_id": "abc123",
    "extracted_info": { ... }
  },
  "message": "简历解析成功"
}
```

### 岗位匹配

```http
POST /api/match-job
Content-Type: application/json

{
  "resume_id": "abc123",
  "job_title": "Python工程师",
  "job_description": "...",
  "required_skills": "Python, FastAPI, MySQL",
  "experience_level": "3-5年"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "total_score": 85,
    "skill_match": { ... },
    "experience_match": { ... },
    "position_match": { ... },
    "recommendations": [ ... ]
  }
}
```

## 🎨 界面展示

### 主界面

- 渐变背景设计
- 响应式布局
- 现代化卡片风格
- 流畅的动画效果

### 候选人卡片

- 金银铜牌排名标识
- 综合评分大字显示
- 技能标签云
- AI评价摘要
- 操作按钮（查看详情、查看PDF）

### 详情弹窗

- 左侧PDF预览
- 右侧详细信息
- 折叠面板展示
- 匹配度可视化（进度条）

## 📊 性能优化

- **前端**：
  - Vite构建优化
  - 代码分割
  - 懒加载
  - 图片优化

- **后端**：
  - 简历缓存机制
  - PDF流式处理
  - API请求超时控制
  - 错误重试机制

## 🔒 安全性

- 环境变量管理API密钥
- CORS跨域配置
- 文件类型验证
- 文件大小限制
- 输入数据验证

## 🐛 已知问题

- PDF扫描件无法识别（需要OCR）
- 加密PDF无法解析
- 超大文件（>4MB）上传限制

## 🔮 未来计划

- [ ] 支持OCR识别扫描件
- [ ] 支持Word格式简历
- [ ] 添加简历模板推荐
- [ ] 支持多语言简历
- [ ] 添加数据统计面板
- [ ] 支持简历导出功能
- [ ] 添加用户认证系统

## 📄 许可证

MIT License

## 👨‍💻 作者

GitHub: [@2464736026](https://github.com/2464736026)

## 🙏 致谢

- OpenAI - 提供强大的GPT模型
- Vercel - 提供优秀的部署平台
- Ant Design - 提供美观的UI组件
- React - 提供高效的前端框架

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：

- GitHub Issues: https://github.com/2464736026/My_Space/issues
- Email: ar2687521@outlook.com

---

**⭐ 如果这个项目对你有帮助，请给个Star支持一下！**
