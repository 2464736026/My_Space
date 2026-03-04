@echo off
chcp 65001 >nul
echo ========================================
echo   阿里云函数计算代码打包工具
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 清理旧的压缩包...
if exist resume-analyzer.zip (
    del resume-analyzer.zip
    echo ✓ 已删除旧压缩包
) else (
    echo ✓ 无需清理
)
echo.

echo [2/3] 打包代码...
powershell -Command "Compress-Archive -Path app,index.py,config.py,requirements.txt -DestinationPath resume-analyzer.zip -Force"

if exist resume-analyzer.zip (
    echo ✓ 打包成功！
    echo.
    echo [3/3] 压缩包信息：
    powershell -Command "Get-Item resume-analyzer.zip | Select-Object Name, @{Name='Size(MB)';Expression={[math]::Round($_.Length/1MB,2)}}"
    echo.
    echo ========================================
    echo   打包完成！
    echo ========================================
    echo.
    echo 📦 文件位置：%cd%\resume-analyzer.zip
    echo.
    echo 📝 下一步操作：
    echo    1. 登录阿里云控制台
    echo    2. 进入函数计算 - 选择你的函数
    echo    3. 点击"代码" - "上传代码" - "上传 ZIP 包"
    echo    4. 选择 resume-analyzer.zip
    echo    5. 点击"部署"按钮
    echo.
    echo 🌐 控制台地址：
    echo    https://fcnext.console.aliyun.com/cn-hangzhou/functions
    echo.
) else (
    echo ✗ 打包失败！
    echo.
    echo 请检查以下文件是否存在：
    echo    - app 目录
    echo    - index.py
    echo    - config.py
    echo    - requirements.txt
    echo.
)

pause
