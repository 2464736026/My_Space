# Vercel 网页端部署教程（图文详解）

## 🌐 通过网页部署前端 - 最简单的方法

命令行部署遇到问题？没关系！通过Vercel网页端部署更简单，只需要点击几下鼠标。

---

## 📋 准备工作

确认以下内容：
- ✅ 代码已推送到GitHub（已完成）
- ✅ 有Vercel账号（你已经登录了）
- ✅ GitHub仓库：`My_Space`

---

## 🚀 详细步骤

### 步骤1：访问Vercel Dashboard

1. 打开浏览器
2. 访问：https://vercel.com/dashboard
3. 确认已登录（看到你的账号名称）

---

### 步骤2：创建新项目

1. 点击右上角的 **"Add New..."** 按钮
2. 在下拉菜单中选择 **"Project"**

![Add New Project](https://vercel.com/docs/concepts/deployments/overview)

---

### 步骤3：导入GitHub仓库

1. 在 "Import Git Repository" 部分
2. 找到 **`My_Space`** 仓库
3. 点击仓库右侧的 **"Import"** 按钮

**如果看不到仓库：**
- 点击 "Adjust GitHub App Permissions"
- 授权Vercel访问你的仓库
- 刷新页面

---

### 步骤4：配置项目（最重要！）

这是最关键的一步，请仔细配置：

#### 4.1 基本设置

| 配置项 | 设置值 |
|--------|--------|
| **Project Name** | `my-space-frontend` （或任意名称）|
| **Framework Preset** | 选择 **"Vite"** |

#### 4.2 Root Directory（关键！）

1. 找到 **"Root Directory"** 配置项
2. 点击右侧的 **"Edit"** 按钮
3. 在弹出的文件选择器中：
   - 点击 **`frontend`** 文件夹
   - 确认选中（文件夹会高亮显示）
   - 点击 **"Continue"** 或 **"Select"**
4. 确认显示为：`frontend`

**⚠️ 重要提示：**
- 必须通过文件选择器选择
- 不要手动输入路径
- 确保显示的是 `frontend` 而不是 `./frontend` 或其他

#### 4.3 构建设置（通常自动检测）

这些设置Vercel会自动检测，通常不需要修改：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| **Build Command** | `npm run build` | 自动检测 |
| **Output Directory** | `dist` | 自动检测 |
| **Install Command** | `npm install` | 自动检测 |

**如果需要手动设置：**
- 点击 "Build and Output Settings" 下的 "Override"
- 填入上述值

#### 4.4 环境变量（可选）

前端不需要环境变量，跳过此步骤。

---

### 步骤5：开始部署

1. 检查所有配置是否正确
2. 点击底部的 **"Deploy"** 按钮
3. 等待部署完成（约2-3分钟）

---

### 步骤6：查看部署进度

部署开始后，你会看到：

1. **Building** - 正在构建
   - 安装依赖
   - 运行构建命令
   - 生成静态文件

2. **Deploying** - 正在部署
   - 上传文件到CDN
   - 配置域名

3. **Ready** - 部署完成 ✅
   - 显示绿色的 "Ready" 状态
   - 显示访问URL

---

### 步骤7：访问你的网站

部署成功后：

1. 在项目页面顶部，你会看到：
   ```
   https://my-space-frontend-xxx.vercel.app
   ```

2. 点击这个URL或复制到浏览器

3. 你应该看到：
   - ✅ AI智能简历分析系统标题
   - ✅ 欢迎页面
   - ✅ 岗位需求配置表单

---

## 🎯 配置检查清单

部署前确认：

- [ ] Project Name: 已填写
- [ ] Framework Preset: 选择了 "Vite"
- [ ] Root Directory: 设置为 `frontend`（通过文件选择器）
- [ ] Build Command: `npm run build`（自动或手动）
- [ ] Output Directory: `dist`（自动或手动）

---

## 🔧 常见问题

### 问题1：找不到 My_Space 仓库

**解决方案：**
1. 点击 "Adjust GitHub App Permissions"
2. 选择 "All repositories" 或选择 `My_Space`
3. 点击 "Save"
4. 返回Vercel，刷新页面

### 问题2：构建失败 - "No package.json found"

**原因：** Root Directory 配置错误

**解决方案：**
1. 进入项目 Settings
2. 找到 "Root Directory"
3. 点击 "Edit"
4. 重新通过文件选择器选择 `frontend` 文件夹
5. 保存后重新部署

### 问题3：构建失败 - 依赖安装错误

**解决方案：**
1. 查看 Build Logs
2. 找到具体错误
3. 通常是依赖版本问题
4. 在项目 Settings → Environment Variables 中添加：
   - `NPM_CONFIG_LEGACY_PEER_DEPS=true`
5. 重新部署

### 问题4：页面显示404

**原因：** 路由配置问题

**解决方案：**
确认 `frontend/vercel.json` 包含：
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

---

## 📊 部署后的操作

### 查看部署详情

1. 在Vercel Dashboard中进入项目
2. 点击 "Deployments" 标签
3. 查看所有部署历史

### 查看构建日志

1. 点击某个部署
2. 查看 "Build Logs" 标签
3. 查看详细的构建过程

### 查看运行日志

1. 点击 "Functions" 标签（如果有）
2. 查看运行时日志

### 自定义域名（可选）

1. 进入项目 Settings
2. 点击 "Domains"
3. 添加自定义域名
4. 按照提示配置DNS

---

## 🎊 成功标志

部署成功后，你会看到：

1. **在Vercel Dashboard：**
   - 项目状态显示 "Ready" 🟢
   - 有一个可访问的URL
   - 最新部署显示 "Production"

2. **访问网站：**
   - 看到完整的前端界面
   - 可以填写岗位需求
   - 可以上传PDF简历
   - 可以查看分析结果

---

## 🔄 后续更新

每次你推送代码到GitHub：
1. Vercel会自动检测
2. 自动重新部署
3. 约2-3分钟后更新生效

---

## 💡 提示

### 快速重新部署

如果需要重新部署：
1. 进入项目页面
2. 点击最新的部署
3. 点击右上角 "..." 菜单
4. 选择 "Redeploy"

### 查看预览部署

每次推送到非主分支：
- Vercel会创建预览部署
- 可以在合并前测试

### 回滚到之前的版本

1. 进入 "Deployments"
2. 找到之前的成功部署
3. 点击 "..." → "Promote to Production"

---

## 📸 关键截图位置

### 配置Root Directory时：

```
┌─────────────────────────────────────┐
│ Root Directory                      │
│ ┌─────────────────────────────────┐ │
│ │ frontend                    Edit│ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

点击 "Edit" 后会看到文件选择器，选择 `frontend` 文件夹。

---

## 🎯 总结

**网页端部署的优势：**
- ✅ 可视化操作，更直观
- ✅ 不需要命令行
- ✅ 自动检测配置
- ✅ 实时查看构建日志
- ✅ 一键重新部署

**关键步骤：**
1. 访问 https://vercel.com/dashboard
2. Add New → Project
3. 导入 `My_Space` 仓库
4. 设置 Root Directory 为 `frontend`
5. 选择 Framework 为 `Vite`
6. 点击 Deploy

**预计时间：** 5分钟

---

## 📞 需要帮助？

如果在网页端部署时遇到问题：

1. **截图当前页面**
   - 包括所有配置项
   - 包括错误信息（如果有）

2. **告诉我：**
   - 在哪一步遇到问题
   - 看到了什么错误
   - 配置是否正确

3. **我会立即帮你解决！**

---

现在就试试吧！通过网页端部署更简单，成功率更高！🚀
