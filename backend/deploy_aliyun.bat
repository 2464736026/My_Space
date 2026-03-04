@echo off
chcp 65001 >nul
echo ========================================
echo   阿里云函数计算一键部署工具
echo ========================================
echo.

cd /d "%~dp0"

echo 📋 部署检查清单
echo.
echo 请确认以下信息：
echo   ✓ 已在阿里云创建服务（例如：resume-analyzer）
echo   ✓ 已在服务中创建函数（例如：api）
echo   ✓ 函数运行环境：Python 3.9 或 3.10
echo   ✓ 函数入口：index.handler
echo   ✓ 内存规格：512MB 或更高
echo   ✓ 超时时间：60 秒
echo.

set /p confirm="是否继续打包？(Y/N): "
if /i not "%confirm%"=="Y" (
    echo 已取消操作
    pause
    exit /b
)

echo.
echo ========================================
echo   开始打包代码
echo ========================================
echo.

echo [1/4] 清理旧文件...
if exist resume-analyzer.zip del resume-analyzer.zip
if exist __pycache__ rmdir /s /q __pycache__
if exist app\__pycache__ rmdir /s /q app\__pycache__
if exist app\services\__pycache__ rmdir /s /q app\services\__pycache__
if exist app\utils\__pycache__ rmdir /s /q app\utils\__pycache__
echo ✓ 清理完成
echo.

echo [2/4] 验证必要文件...
set missing=0

if not exist "app\main.py" (
    echo ✗ 缺少文件：app\main.py
    set missing=1
)
if not exist "index.py" (
    echo ✗ 缺少文件：index.py
    set missing=1
)
if not exist "config.py" (
    echo ✗ 缺少文件：config.py
    set missing=1
)
if not exist "requirements.txt" (
    echo ✗ 缺少文件：requirements.txt
    set missing=1
)

if %missing%==1 (
    echo.
    echo ✗ 缺少必要文件，无法继续
    pause
    exit /b 1
)

echo ✓ 所有必要文件存在
echo.

echo [3/4] 打包代码...
powershell -Command "Compress-Archive -Path app,index.py,config.py,requirements.txt -DestinationPath resume-analyzer.zip -Force"

if not exist resume-analyzer.zip (
    echo ✗ 打包失败
    pause
    exit /b 1
)

echo ✓ 打包成功
echo.

echo [4/4] 压缩包信息：
powershell -Command "Get-Item resume-analyzer.zip | Format-Table Name, @{Name='大小(MB)';Expression={[math]::Round($_.Length/1MB,2)}}, LastWriteTime -AutoSize"
echo.

echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 📦 压缩包位置：
echo    %cd%\resume-analyzer.zip
echo.
echo 📝 接下来的步骤：
echo.
echo 1️⃣  上传代码包到阿里云
echo    - 访问：https://fcnext.console.aliyun.com/cn-hangzhou/functions
echo    - 选择你的函数（例如：api）
echo    - 点击"代码"标签
echo    - 点击"上传代码" → "上传 ZIP 包"
echo    - 选择 resume-analyzer.zip
echo    - 点击"部署"按钮（重要！）
echo.
echo 2️⃣  配置环境变量（如果还没配置）
echo    - 在函数详情页点击"配置"标签
echo    - 找到"环境变量"部分
echo    - 添加以下变量：
echo      OPENAI_API_KEY = sk-R4Z3s07Fvg0nuvLlLtmMNe7EGRhv8DLhmlicxy9x6tEPRd7m
echo      OPENAI_MODEL = gpt-3.5-turbo
echo      OPENAI_BASE_URL = https://api.openai-proxy.org/v1
echo    - 点击"保存"并重新"部署"
echo.
echo 3️⃣  测试部署
echo    - 在"触发器"标签中复制"公网访问地址"
echo    - 在浏览器中访问该地址
echo    - 应该看到：{"message": "AI Resume Analyzer API", "version": "1.0.0"}
echo.
echo 4️⃣  更新前端配置
echo    - 编辑 frontend\src\App.jsx
echo    - 将 API_BASE_URL 更新为你的FC地址
echo    - 提交代码到GitHub
echo.
echo ========================================
echo.

set /p open="是否打开阿里云控制台？(Y/N): "
if /i "%open%"=="Y" (
    start https://fcnext.console.aliyun.com/cn-hangzhou/functions
)

echo.
pause
