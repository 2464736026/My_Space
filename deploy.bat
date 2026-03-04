@echo off
chcp 65001 >nul
echo ==========================================
echo   AI智能简历分析系统 - 部署脚本
echo ==========================================
echo.

REM 检查Git仓库
echo [1/5] 检查Git仓库...
if not exist ".git" (
    echo 错误: 未找到Git仓库，请先初始化Git
    echo 运行: git init
    pause
    exit /b 1
)
echo √ Git仓库已就绪
echo.

REM 检查API密钥配置
echo [2/5] 检查API密钥配置...
findstr /C:"your-openai-api-key-here" backend\config.py >nul
if %errorlevel% equ 0 (
    echo 错误: 请先在 backend\config.py 中配置OpenAI API密钥
    pause
    exit /b 1
)
echo √ API密钥已配置
echo.

REM 提交代码到GitHub
echo [3/5] 提交代码到GitHub...
set /p commit_msg="请输入提交信息 (默认: Update deployment): "
if "%commit_msg%"=="" set commit_msg=Update deployment

git add .
git commit -m "%commit_msg%"

REM 检查是否有远程仓库
git remote | findstr "origin" >nul
if %errorlevel% neq 0 (
    echo 未找到远程仓库，请输入GitHub仓库地址:
    set /p repo_url="GitHub仓库地址 (例: https://github.com/username/repo.git): "
    git remote add origin "%repo_url%"
)

git push origin main
echo √ 代码已推送到GitHub
echo.

REM 部署到阿里云FC
echo [4/5] 部署后端到阿里云函数计算...
echo 请确保已安装并配置 Funcraft 工具
echo 如未安装，运行: npm install @alicloud/fun -g
echo 如未配置，运行: fun config
echo.
set /p deploy_fc="是否继续部署到阿里云FC? (y/n): "

if /i "%deploy_fc%"=="y" (
    cd backend
    call fun deploy
    cd ..
    echo √ 后端已部署到阿里云FC
) else (
    echo 跳过阿里云FC部署
)
echo.

REM GitHub Pages部署提示
echo [5/5] GitHub Pages部署...
echo GitHub Actions会自动部署前端到GitHub Pages
echo 请访问: https://github.com/你的用户名/你的仓库名/actions
echo 查看部署进度
echo.
echo 部署完成后，访问以下地址:
echo 前端: https://你的用户名.github.io/resume-analyzer/
echo 后端: 查看阿里云FC控制台获取HTTP触发器地址
echo.

echo ==========================================
echo   部署流程完成！
echo ==========================================
echo.
echo 下一步:
echo 1. 在GitHub仓库中启用GitHub Pages (Settings → Pages)
echo 2. 更新 frontend\src\App.jsx 中的 API_BASE_URL 为阿里云FC地址
echo 3. 再次推送代码: git push origin main
echo 4. 等待GitHub Actions自动部署
echo.
echo 详细说明请查看: DEPLOYMENT_GUIDE.md
echo.
pause
