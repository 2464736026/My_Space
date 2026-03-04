# 🚀 简单部署指南

> 3步完成阿里云函数计算部署

---

## 第一步：打包代码 📦

### Windows 用户

双击运行：
```
backend\deploy_aliyun.bat
```

或在命令行中：
```cmd
cd backend
deploy_aliyun.bat
```

这会自动创建 `resume-analyzer.zip` 文件。

---

## 第二步：上传到阿里云 ☁️

### 1. 登录阿里云控制台

访问：https://fcnext.console.aliyun.com/cn-hangzhou/functions

### 2. 选择你的函数

点击你创建的函数（例如：`api`）

### 3. 上传代码包

1. 点击"代码"标签
2. 点击"上传代码" → "上传 ZIP 包"
3. 选择 `backend\resume-analyzer.zip`
4. 等待上传完成
5. **重要**：点击"部署"按钮！

### 4. 配置环境变量（首次部署需要）

1. 点击"配置"标签
2. 找到"环境变量"部分
3. 点击"编辑"
4. 添加以下3个环境变量：

| 变量名 | 变量值 |
|--------|--------|
| `OPENAI_API_KEY` | `sk-R4Z3s07Fvg0nuvLlLtmMNe7EGRhv8DLhmlicxy9x6tEPRd7m` |
| `OPENAI_MODEL` | `gpt-3.5-turbo` |
| `OPENAI_BASE_URL` | `https://api.openai-proxy.org/v1` |

5. 点击"保存"
6. 再次点击"部署"

### 5. 确认基本配置

在"配置"标签中确认：

- **函数入口**：`index.handler` ✅
- **运行环境**：`Python 3.10` 或 `Python 3.9` ✅
- **内存规格**：`512 MB` 或更高 ✅
- **超时时间**：`60 秒` ✅

如果不对，点击"编辑"修改，然后"保存"并"部署"。

---

## 第三步：测试部署 🧪

### 1. 获取函数URL

在"触发器"标签中，复制"公网访问地址"，例如：
```
https://1234567890.cn-hangzhou.fc.aliyuncs.com/2016-08-15/proxy/resume-analyzer/api/
```

### 2. 测试访问

在浏览器中打开这个地址，应该看到：

```json
{
  "message": "AI Resume Analyzer API",
  "version": "1.0.0"
}
```

✅ 如果看到这个，说明部署成功！

❌ 如果看到错误，请查看下面的"常见问题"部分。

### 3. 测试API文档

访问：`你的FC地址/docs`

应该能看到 Swagger API 文档界面。

---

## 🎯 部署成功后的下一步

### 1. 更新前端配置

编辑 `frontend/src/App.jsx`，找到第47-50行：

```javascript
// 修改前
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://your-fc-domain.com' 
  : 'http://localhost:8000';

// 修改后（替换为你的FC地址）
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://你的FC地址' 
  : 'http://localhost:8000';
```

**注意**：不要在URL末尾加 `/`

### 2. 提交代码到GitHub

```bash
git add frontend/src/App.jsx
git commit -m "Update: configure Aliyun FC API URL"
git push origin main
```

### 3. 部署前端到GitHub Pages

1. 在GitHub仓库页面，点击"Settings"
2. 在左侧菜单找到"Pages"
3. 在"Source"下选择分支（通常是 `main`）
4. 点击"Save"
5. 等待几分钟，GitHub会提供一个访问地址

---

## ❌ 常见问题

### Q1: 上传后访问显示错误

**检查清单**：
- [ ] 是否点击了"部署"按钮？（上传后必须部署）
- [ ] 函数入口是否为 `index.handler`？
- [ ] 环境变量是否配置正确？
- [ ] 配置修改后是否重新部署？

**解决方法**：
1. 在函数详情页点击"日志查询"
2. 查看最近的错误日志
3. 根据错误信息修正

### Q2: 显示 "required HTTP header Date was not specified"

**原因**：`index.py` 文件不完整

**解决**：
1. 在阿里云控制台，点击"代码"标签
2. 打开 `index.py` 文件
3. 检查文件是否完整（应该有约98行）
4. 如果不完整，重新上传代码包

### Q3: 显示 "Module not found: app.main"

**原因**：目录结构不正确

**解决**：
1. 确保压缩包包含 `app` 目录
2. 确保 `app/main.py` 存在
3. 重新打包上传

### Q4: 超时错误

**解决**：
1. 增加超时时间到 60 秒
2. 增加内存到 1024 MB

### Q5: CORS 错误

**解决**：
1. 在"触发器"标签中，点击HTTP触发器的"编辑"
2. 在"高级配置"中配置CORS：
   - 允许的源：`*`
   - 允许的方法：`GET, POST, PUT, DELETE, OPTIONS`
   - 允许的头：`*`

---

## 📞 需要帮助？

### 查看日志

1. 在函数详情页点击"日志查询"
2. 选择时间范围
3. 查看详细错误信息

### 重新部署

如果遇到问题，可以：
1. 重新运行 `deploy_aliyun.bat` 打包
2. 重新上传代码包
3. 确保点击"部署"
4. 清除浏览器缓存后重试

---

## ✅ 部署检查清单

部署前确认：

- [ ] 运行了 `deploy_aliyun.bat` 并生成了 `resume-analyzer.zip`
- [ ] 在阿里云控制台上传了代码包
- [ ] 点击了"部署"按钮
- [ ] 函数入口设置为 `index.handler`
- [ ] 配置了3个环境变量
- [ ] 内存至少 512MB，超时时间 60秒
- [ ] 测试访问根路径返回正确JSON
- [ ] 更新了前端的 API_BASE_URL
- [ ] 提交了代码到GitHub

---

**就这么简单！** 🎉

如果遇到问题，查看 `backend/PACK_INSTRUCTIONS.md` 获取更详细的说明。
