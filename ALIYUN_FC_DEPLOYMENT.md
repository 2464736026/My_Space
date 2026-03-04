# 阿里云函数计算部署指南

> 详细的阿里云FC部署步骤

---

## 📋 准备工作

### 1. 安装 Serverless Devs（推荐）

Funcraft 已经过时，使用新的 Serverless Devs 工具：

```bash
# 安装 Serverless Devs
npm install -g @serverless-devs/s

# 验证安装
s --version
```

### 2. 配置阿里云账号

```bash
s config add

# 按提示输入：
# - AccountID: 你的阿里云账号ID（在控制台右上角查看）
# - AccessKeyID: 访问密钥ID
# - AccessKeySecret: 访问密钥Secret
# - 选择默认区域: cn-hangzhou
```

**获取 AccessKey：**
1. 登录阿里云控制台
2. 访问：https://ram.console.aliyun.com/manage/ak
3. 创建 AccessKey 并保存

---

## 🚀 方案一：使用 Serverless Devs 部署（推荐）

### 步骤1：进入后端目录

```bash
cd backend
```

### 步骤2：部署

```bash
s deploy
```

部署成功后会显示HTTP触发器地址，例如：
```
https://1234567890.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/resume-analyzer/api/
```

### 步骤3：测试

```bash
# 测试健康检查
curl https://你的FC地址/

# 应该返回：
# {"message": "AI Resume Analyzer API", "version": "1.0.0"}
```

---

## 🚀 方案二：使用阿里云控制台部署

如果命令行工具有问题，可以直接使用控制台：

### 步骤1：打包代码

```bash
cd backend

# 安装依赖到本地
pip install -r requirements.txt -t .

# 打包（Windows）
powershell Compress-Archive -Path * -DestinationPath ../resume-analyzer.zip

# 或使用 7-Zip
7z a -tzip ../resume-analyzer.zip *
```

### 步骤2：登录阿里云控制台

1. 访问：https://fc.console.aliyun.com/
2. 选择区域：华东1（杭州）

### 步骤3：创建服务

1. 点击"服务及函数" → "创建服务"
2. 填写信息：
   - 服务名称：`resume-analyzer`
   - 描述：`AI Resume Analyzer Service`
   - 网络配置：允许访问公网
3. 点击"创建"

### 步骤4：创建函数

1. 在服务中点击"创建函数"
2. 选择"使用标准 Runtime 创建"
3. 填写信息：
   - 函数名称：`api`
   - 运行环境：`Python 3.10`
   - 代码上传方式：选择"上传代码包"
   - 上传 `resume-analyzer.zip`
   - 函数入口：`index.handler`
   - 内存规格：`1024 MB`
   - 超时时间：`60 秒`

### 步骤5：配置环境变量

在函数配置中添加环境变量：
```
OPENAI_API_KEY = sk-R4Z3s07Fvg0nuvLlLtmMNe7EGRhv8DLhmlicxy9x6tEPRd7m
OPENAI_MODEL = gpt-3.5-turbo
OPENAI_BASE_URL = https://api.openai-proxy.org/v1
```

### 步骤6：创建HTTP触发器

1. 在函数页面点击"触发器"标签
2. 点击"创建触发器"
3. 填写信息：
   - 触发器类型：`HTTP触发器`
   - 触发器名称：`httpTrigger`
   - 请求方式：选择所有（GET, POST, PUT, DELETE, OPTIONS）
   - 鉴权方式：`anonymous`（匿名）
4. 点击"确定"

### 步骤7：获取访问地址

创建触发器后，会显示公网访问地址，例如：
```
https://1234567890.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/resume-analyzer/api/
```

**复制这个地址！**

---

## 🔧 配置 CORS

### 在函数计算控制台配置

1. 进入函数详情页
2. 点击"触发器"标签
3. 点击HTTP触发器的"编辑"
4. 在"高级配置"中添加CORS：
   ```
   允许的源：*
   允许的方法：GET, POST, PUT, DELETE, OPTIONS
   允许的头：*
   暴露的头：*
   最大缓存时间：3600
   ```

---

## 🧪 测试部署

### 1. 测试健康检查

```bash
curl https://你的FC地址/
```

应该返回：
```json
{"message": "AI Resume Analyzer API", "version": "1.0.0"}
```

### 2. 测试API文档

访问：`https://你的FC地址/docs`

应该能看到 Swagger API 文档。

### 3. 测试上传接口

```bash
curl -X POST "https://你的FC地址/api/upload-resume" \
  -F "file=@test_resume.pdf"
```

---

## 📝 更新前端配置

部署成功后，更新前端API地址：

### 编辑 `frontend/src/App.jsx`

找到这一行：
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

### 提交更改

```bash
git add frontend/src/App.jsx
git commit -m "Update: configure Aliyun FC API URL"
git push origin main
```

---

## ❓ 常见问题

### Q1: 部署后访问返回 502

**原因**：函数执行超时或内存不足

**解决**：
1. 增加内存到 1024MB 或更高
2. 增加超时时间到 60秒
3. 检查日志查看具体错误

### Q2: 提示权限不足

**原因**：AccessKey 权限不够

**解决**：
1. 在RAM控制台给用户添加 `AliyunFCFullAccess` 权限
2. 或使用主账号的 AccessKey

### Q3: 依赖包太大无法上传

**原因**：代码包超过 50MB

**解决方案A - 使用层（Layer）**：
1. 将依赖打包为层
2. 在函数中引用层

**解决方案B - 使用 OSS**：
1. 将代码包上传到 OSS
2. 从 OSS 部署函数

### Q4: CORS 错误

**原因**：未配置 CORS

**解决**：
1. 在HTTP触发器中配置CORS
2. 或在代码中添加CORS中间件（已添加）

---

## 💰 成本估算

阿里云函数计算按量付费：

- **调用次数**：前100万次免费，之后 ¥0.0000002/次
- **执行时长**：前40万GB-秒免费，之后 ¥0.00003334/GB-秒
- **流量**：前10GB免费，之后 ¥0.50/GB

**示例**：
- 每次请求约 10秒，使用 1GB 内存
- 100次请求 = 1000 GB-秒 ≈ ¥0.03
- 1000次请求 ≈ ¥0.30

基本上免费额度足够测试和演示使用。

---

## 📞 需要帮助？

如果遇到问题：

1. **查看函数日志**：
   - 在函数计算控制台
   - 点击"日志查询"
   - 查看详细错误信息

2. **检查配置**：
   - 环境变量是否正确
   - 内存和超时设置是否足够
   - HTTP触发器是否正确配置

3. **测试本地**：
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
   确保本地运行正常

---

## ✅ 部署检查清单

- [ ] 安装了 Serverless Devs 或准备使用控制台
- [ ] 配置了阿里云 AccessKey
- [ ] 代码已打包（如使用控制台）
- [ ] 创建了服务和函数
- [ ] 配置了环境变量
- [ ] 创建了HTTP触发器
- [ ] 配置了CORS
- [ ] 测试了API接口
- [ ] 更新了前端API地址
- [ ] 推送了代码到GitHub

---

**现在开始部署吧！** 🚀

推荐使用 **Serverless Devs** 方式，更简单快捷。如果遇到问题，可以使用控制台方式。
