# AI智能简历分析系统

> 基于OpenAI GPT的智能简历筛选与岗位匹配系统

## 📋 项目简介

这是一个完整的AI驱动简历分析系统，支持批量上传PDF简历，自动提取关键信息，并根据岗位需求进行智能匹配和排序。

### 核心功能

- ✅ **批量简历上传** - 支持同时上传多份PDF简历
- ✅ **AI智能提取** - 使用OpenAI GPT自动提取简历关键信息
- ✅ **岗位匹配分析** - 三维评分（技能50% + 经验30% + 职位20%）
- ✅ **智能排序** - 按匹配度自动排序候选人
- ✅ **PDF预览** - 支持在线预览原始PDF文件
- ✅ **详细分析报告** - 提供完整的匹配度分析和改进建议

## 🛠 技术栈

### 后端
- **Python 3.8+** + FastAPI
- **OpenAI GPT-3.5-turbo** / GPT-4
- **pdfplumber** + PyPDF2 (PDF解析)
- **内存缓存** (可扩展Redis)

### 前端
- **React 18** + Vite
- **Ant Design** (UI组件库)
- **Axios** (HTTP客户端)

## 🚀 快速开始

### 本地开发

#### 1. 环境要求

- Python 3.8+
- Node.js 14+
- OpenAI API密钥

#### 2. 获取OpenAI API密钥

1. 访问 https://platform.openai.com/api-keys
2. 注册/登录账号
3. 创建新密钥
4. 复制密钥（格式：`sk-...`）

#### 3. 配置API密钥

编辑 `backend/config.py`：

```python
OPENAI_API_KEY = "sk-your-actual-api-key-here"  # 替换为你的密钥
OPENAI_MODEL = "gpt-3.5-turbo"  # 或 "gpt-4"
```

详细配置说明请查看 `backend/API_KEY_SETUP.md`

#### 4. 安装依赖

```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd frontend
npm install
```

#### 5. 启动服务

**方式一：使用启动脚本（推荐）**

```bash
python start_dev.py
```

**方式二：手动启动**

```bash
# 终端1 - 后端
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 终端2 - 前端
cd frontend
npm run dev
```

#### 6. 访问应用

- 前端：http://localhost:5173/resume-analyzer/
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

### 部署到 Vercel

详细部署指南请查看: [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md)

**快速部署步骤:**

1. 推送代码到 GitHub
2. 在 Vercel 导入项目
3. 配置环境变量 (OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL)
4. 点击部署
5. 更新前端 API 地址

**优势:**
- ✅ 自动部署 - 推送到 GitHub 自动部署
- ✅ 免费额度 - 个人项目完全免费
- ✅ 全球 CDN - 访问速度快
- ✅ 简单配置 - 无需配置服务器

## 📖 使用流程

### 步骤1：配置岗位需求

填写招聘岗位信息：
- 职位名称（必填）
- 经验要求（必填）
- 技能要求（必填）
- 职位描述（必填）

### 步骤2：批量上传简历

- 支持同时上传多份PDF文件
- 系统自动逐个分析
- 实时显示分析进度

### 步骤3：查看分析结果

- 候选人按评分自动排序
- 前三名特殊标识（🥇🥈🥉）
- 点击卡片查看详细信息
- 点击"查看PDF"预览原文件

## 🎯 评分系统

### 综合评分算法

```
综合评分 = 技能匹配度 × 50% + 经验匹配度 × 30% + 职位匹配度 × 20%
```

### 面试建议

- **80分以上** - 强烈推荐进入面试
- **60-79分** - 建议进入面试
- **60分以下** - 暂不推荐

## 📁 项目结构

```
ai-resume-analyzer/
├── api/
│   └── index.py              # Vercel 入口文件
│
├── backend/                   # 后端服务
│   ├── app/
│   │   ├── main.py           # FastAPI主程序
│   │   ├── services/
│   │   │   ├── pdf_parser.py # PDF解析
│   │   │   └── ai_service.py # AI服务（核心）
│   │   └── utils/
│   │       └── cache.py      # 缓存管理
│   ├── config.py             # ⭐ API配置（需填写）
│   └── requirements.txt      # Python依赖
│
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── App.jsx          # 主组件
│   │   ├── index.css        # 样式
│   │   └── main.jsx         # 入口
│   └── package.json         # Node依赖
│
├── vercel.json               # Vercel 配置
├── start_dev.py             # 本地启动脚本
└── README.md                # 项目说明（本文件）
```

## 💰 成本估算

### GPT-3.5-turbo（推荐）
- 每份简历分析：约 $0.002-0.005
- 每次岗位匹配：约 $0.003-0.007
- 100次完整流程：约 $0.50-1.20

### GPT-4（高精度）
- 每份简历分析：约 $0.05-0.15
- 每次岗位匹配：约 $0.08-0.20
- 100次完整流程：约 $13-35

## 🧪 测试

### 测试API

```bash
cd backend
python test_api.py
```

### 测试流程

1. 启动服务
2. 访问前端页面
3. 配置岗位需求
4. 上传测试PDF简历
5. 查看分析结果

## 🔧 配置说明

### OpenAI API配置

在 `backend/config.py` 中配置：

```python
# API密钥（必需）
OPENAI_API_KEY = "sk-..."

# 模型选择
OPENAI_MODEL = "gpt-3.5-turbo"  # 或 "gpt-4"

# 代理设置（可选）
OPENAI_BASE_URL = None  # 或 "https://your-proxy.com/v1"

# 调用参数
MAX_TOKENS = 2000      # 返回token数
TEMPERATURE = 0.1      # 确定性（0-2）
TIMEOUT = 30           # 超时时间（秒）
```

详细说明：`backend/API_KEY_SETUP.md`

## 🐛 常见问题

### Q: 提示"请配置OPENAI_API_KEY"
**A:** 检查 `backend/config.py` 文件是否存在且密钥正确

### Q: PDF上传后无响应
**A:** 
1. 确认PDF文件未损坏
2. 检查PDF包含可提取的文本（非扫描件）
3. 查看浏览器控制台错误信息

### Q: AI提取结果不准确
**A:**
1. 尝试使用 GPT-4 模型
2. 优化提示词（在 `config.py` 中）
3. 检查简历格式是否规范

### Q: 前端无法连接后端
**A:**
1. 确认后端服务正在运行（http://localhost:8000）
2. 检查端口8000是否被占用
3. 查看后端终端错误信息

## 📚 相关文档

- [Vercel 部署指南](VERCEL_DEPLOYMENT_GUIDE.md) - 完整的 Vercel 部署流程
- [API密钥配置指南](backend/API_KEY_SETUP.md) - OpenAI API配置详解

## 🎓 技术亮点

1. **完全AI驱动** - 使用OpenAI GPT替代传统规则提取
2. **批量处理** - 支持同时上传多份简历，自动队列处理
3. **智能排序** - 按AI评分自动排序，一目了然
4. **PDF预览** - 支持在线预览和新标签页打开
5. **响应式设计** - 适配各种屏幕尺寸
6. **现代化UI** - 渐变背景、玻璃态效果、流畅动画

## 📄 许可证

MIT License

## 👨‍💻 作者

本项目为技术面试作品，展示了完整的全栈开发能力和AI集成技术。

---

**开始使用：**

```bash
# 1. 配置API密钥（编辑 backend/config.py）
# 2. 安装依赖
cd backend && pip install -r requirements.txt
cd frontend && npm install

# 3. 启动服务
python start_dev.py

# 4. 访问应用
# http://localhost:5173/resume-analyzer/
```

🚀 祝你使用愉快！
