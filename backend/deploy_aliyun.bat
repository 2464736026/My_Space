@echo off
chcp 65001 >nul
echo ========================================
echo   阿里云函数计算打包工具
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 清理旧文件...
if exist resume-analyzer.zip del resume-analyzer.zip
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
if exist app\__pycache__ rmdir /s /q app\__pycache__ 2>nul
if exist app\services\__pycache__ rmdir /s /q app\services\__pycache__ 2>nul
if exist app\utils\__pycache__ rmdir /s /q app\utils\__pycache__ 2>nul
echo ✓ 清理完成
echo.

echo [2/3] 打包代码...
powershell -Command "Compress-Archive -Path app,index.py,config.py,requirements.txt -DestinationPath resume-analyzer.zip -Force"

if not exist resume-analyzer.zip (
    echo ✗ 打包失败
    pause
    exit /b 1
)

echo ✓ 打包成功
echo.

echo [3/3] 压缩包信息：
powershell -Command "Get-Item resume-analyzer.zip | Select-Object Name, @{Name='大小(MB)';Expression={[math]::Round($_.Length/1MB,2)}}"
echo.

echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 📦 文件：%cd%\resume-analyzer.zip
echo.
echo 📝 下一步：
echo    1. 访问阿里云控制台
echo    2. 上传 resume-analyzer.zip
echo    3. 点击"部署"
echo.
echo 详细步骤请查看：DEPLOY_GUIDE.md
echo.

pause
