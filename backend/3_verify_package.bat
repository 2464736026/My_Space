@echo off
chcp 65001 >nul
echo ========================================
echo   步骤3：验证打包内容
echo ========================================
echo.

cd /d "%~dp0"

if not exist resume-analyzer.zip (
    echo ✗ 找不到 resume-analyzer.zip
    echo.
    echo 请先运行 2_package.bat 进行打包
    pause
    exit /b 1
)

echo 检查 ZIP 包内容...
echo.

powershell -Command "Add-Type -AssemblyName System.IO.Compression.FileSystem; $zip = [System.IO.Compression.ZipFile]::OpenRead('resume-analyzer.zip'); Write-Host '=== ZIP 包内容 ==='; Write-Host ''; $zip.Entries | Select-Object FullName | Format-Table -AutoSize; $zip.Dispose()"

echo.
echo ========================================
echo   验证要点
echo ========================================
echo.
echo 必须包含以下目录/文件：
echo   ✓ app/
echo   ✓ python/          ← 最重要！
echo   ✓ index.py
echo   ✓ config.py
echo.
echo 如果缺少 python/ 目录：
echo   1. 确认 backend\python 目录存在
echo   2. 重新运行 2_package.bat
echo.

pause
