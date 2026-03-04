# 阿里云 FC 配置说明

## 问题分析

经过多次尝试，发现阿里云函数计算的 HTTP 触发器与标准 WSGI 协议存在兼容性问题。

## ✅ 新方案：使用事件函数格式

我已经将 `index.py` 改为使用阿里云 FC 的**事件函数格式**：

```python
def handler(event, context):
    """事件函数处理器"""
    # 从 event 中解析 HTTP 请求
    # 返回 HTTP 响应对象
    return {
        'statusCode': 200,
        'headers': {...},
        'body': '...'
    }
```

---

## 📝 部署步骤

### 第一步：重新打包

```cmd
cd backend
deploy_aliyun.bat
```

### 第二步：修改触发器配置

这是关键步骤！

1. 访问：https://fcnext.console.aliyun.com/cn-hangzhou/functions
2. 选择函数 `api`
3. 点击"触发器"标签
4. **删除现有的 HTTP 触发器**
5. 点击"创建触发器"
6. 选择触发器类型：**HTTP 触发器**
7. 配置：
   - 触发器名称：`httpTrigger`
   - 请求方式：全选
   - 鉴权方式：`anonymous`
   - **请求模式**：选择 **"返回响应"** 或 **"事件格式"**
8. 点击"确定"

### 第三步：上传代码

1. 点击"代码"标签
2. 上传 `resume-analyzer.zip`
3. 点击"部署"

### 第四步：测试

访问：`https://api-lanxianlei.cn-hangzhou.fcapp.run/`

---

## 🔍 如果还是失败

### 方案A：查看详细日志

请截图以下内容：

1. **函数日志**（"日志查询"标签）
2. **触发器配置**（"触发器"标签）
3. **浏览器控制台错误**（F12 → Console 标签）

### 方案B：尝试 API 网关

如果 HTTP 触发器始终有问题，可以改用 API 网关：

1. 在阿里云控制台搜索"API 网关"
2. 创建 API 分组
3. 创建 API，后端服务选择"函数计算"
4. 绑定到你的函数
5. 使用 API 网关提供的地址

### 方案C：使用 Custom Runtime

阿里云 FC 支持 Custom Runtime，可以直接运行 HTTP 服务器：

1. 修改函数配置
2. 运行环境选择：`Custom Runtime`
3. 启动命令：`uvicorn app.main:app --host 0.0.0.0 --port 9000`

---

## 💡 建议

如果阿里云 FC 持续有问题，建议考虑：

1. **使用腾讯云函数**（对 Python WSGI 支持更好）
2. **使用 Vercel**（免费，支持 Python，部署简单）
3. **使用 Railway**（免费额度，支持 Docker）
4. **使用阿里云 ECS**（虚拟机，完全控制）

---

**请先尝试新的事件函数格式，如果还是失败，请提供详细日志。** 🔍
