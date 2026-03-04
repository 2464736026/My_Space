@echo off
chcp 65001 >nul
echo ========================================
echo   步骤2：打包代码
echo ========================================
echo.

cd /d "%~dp0"

echo 检查依赖目录...
if not exist python (
    echo ✗ 依赖目录不存在
    echo.
    echo 请先运行 1_install_deps.bat 安装依赖
    echo.
    pause
    exit /b 1
)
echo ✓ 依赖目录存在
echo.

echo 清理旧的压缩包...
if exist resume-analyzer.zip del resume-analyzer.zip
echo.

echo 清理缓存文件...
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
if exist app\__pycache__ rmdir /s /q app\__pycache__ 2>nul
if exist app\services\__pycache__ rmdir /s /q app\services\__pycache__ 2>nul
if exist app\utils\__pycache__ rmdir /s /q app\utils\__pycache__ 2>nul
echo.

echo 开始打包...
powershell -Command "Compress-Archive -Path app,index.py,config.py,python -DestinationPath resume-analyzer.zip -Force"

if not exist resume-analyzer.zip (
    echo ✗ 打包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo   打包完成！
echo ========================================
echo.

powershell -Command "Get-Item resume-analyzer.zip | Select-Object Name, @{Name='大小(MB)';Expression={[math]::Round($_.Length/1MB,2)}}"

echo.
echo 📦 文件：%cd%\resume-analyzer.zip
echo.
echo 📝 下一步：
echo    1. 访问阿里云控制台
echo    2. 上传 resume-analyzer.zip
echo    3. 点击"部署"
echo.

pause
