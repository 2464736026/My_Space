# OpenAI API密钥配置指南

## 📝 配置步骤

### 1. 获取OpenAI API密钥

1. 访问 OpenAI 官网：https://platform.openai.com/
2. 注册/登录账号
3. 进入 API Keys 页面：https://platform.openai.com/api-keys
4. 点击 "Create new secret key" 创建新密钥
5. 复制生成的密钥（格式类似：`sk-...`）

### 2. 配置API密钥

打开文件：`backend/config.py`

找到这一行：
```python
OPENAI_API_KEY = "your-openai-api-key-here"
```

替换为你的实际API密钥：
```python
OPENAI_API_KEY = "sk-your-actual-api-key-here"
```

### 3. 选择模型（可选）

默认使用 `gpt-3.5-turbo`，如果需要更好的效果，可以改为 `gpt-4`：

```python
OPENAI_MODEL = "gpt-4"  # 更准确但更贵
```

### 4. 配置代理（可选）

如果需要使用代理访问OpenAI API，可以设置：

```python
OPENAI_BASE_URL = "https://your-proxy-url.com/v1"
```

## 💰 费用说明

### GPT-3.5-turbo 定价
- 输入：$0.0005 / 1K tokens
- 输出：$0.0015 / 1K tokens

### GPT-4 定价
- 输入：$0.03 / 1K tokens
- 输出：$0.06 / 1K tokens

### 预估成本
- 每份简历分析：约 1000-2000 tokens
- 每次岗位匹配：约 1500-2500 tokens
- 使用 GPT-3.5-turbo：每次分析约 $0.002-0.005
- 使用 GPT-4：每次分析约 $0.05-0.15

## 🔧 配置参数说明

### MAX_TOKENS
```python
MAX_TOKENS = 2000  # AI返回的最大token数
```
- 建议值：1500-3000
- 太小可能导致返回不完整
- 太大会增加成本

### TEMPERATURE
```python
TEMPERATURE = 0.1  # 温度参数
```
- 范围：0-2
- 0：最确定的输出
- 1：平衡创造性和确定性
- 2：最有创造性的输出
- 建议：0.1-0.3（信息提取任务需要确定性）

### TIMEOUT
```python
TIMEOUT = 30  # 请求超时时间（秒）
```
- 建议值：20-60秒
- 网络较慢时可以增加

## ⚠️ 安全提示

1. **不要将API密钥提交到Git**
   - 已在 `.gitignore` 中排除 `config.py`
   - 使用环境变量更安全

2. **定期轮换密钥**
   - 建议每3-6个月更换一次

3. **监控使用量**
   - 在 OpenAI 控制台查看使用情况
   - 设置使用限额

4. **使用环境变量（推荐）**
   ```python
   import os
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-default-key")
   ```

## 🧪 测试配置

配置完成后，运行测试：

```bash
cd backend
python -c "from app.services.ai_service import AIService; ai = AIService(); print('配置成功！')"
```

如果看到 "配置成功！"，说明配置正确。

## 🐛 常见问题

### Q1: 提示 "请配置 OPENAI_API_KEY"
**解决**：检查 `config.py` 中的密钥是否正确填写

### Q2: 提示 "Incorrect API key"
**解决**：
1. 检查密钥是否完整复制
2. 确认密钥未过期
3. 检查账户是否有余额

### Q3: 提示 "Rate limit exceeded"
**解决**：
1. 等待一段时间后重试
2. 升级到付费账户
3. 降低请求频率

### Q4: 提示 "Connection timeout"
**解决**：
1. 检查网络连接
2. 增加 TIMEOUT 值
3. 配置代理

### Q5: 返回结果不准确
**解决**：
1. 尝试使用 GPT-4 模型
2. 调整 TEMPERATURE 参数
3. 优化提示词（在 config.py 中）

## 📚 相关链接

- OpenAI API 文档：https://platform.openai.com/docs
- API 密钥管理：https://platform.openai.com/api-keys
- 使用量查看：https://platform.openai.com/usage
- 定价信息：https://openai.com/pricing

---

**配置完成后，请重启后端服务！**

```bash
# 停止当前服务（Ctrl+C）
# 重新启动
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
