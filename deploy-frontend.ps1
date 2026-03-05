# 前端部署脚本
# 使用方法: .\deploy-frontend.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI简历分析系统 - 前端部署" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查当前目录
$currentDir = Get-Location
Write-Host "当前目录: $currentDir" -ForegroundColor Yellow

# 检查frontend目录
if (-not (Test-Path "frontend")) {
    Write-Host "错误: 请在项目根目录运行此脚本" -ForegroundColor Red
    Write-Host "正确路径: E:\newP" -ForegroundColor Yellow
    exit 1
}

# 进入frontend目录
Write-Host "进入frontend目录..." -ForegroundColor Yellow
Set-Location frontend

# 检查package.json
if (-not (Test-Path "package.json")) {
    Write-Host "错误: package.json不存在" -ForegroundColor Red
    exit 1
}

Write-Host "✓ package.json存在" -ForegroundColor Green
Write-Host ""

# 检查Vercel CLI
try {
    $vercelVersion = vercel --version 2>&1
    Write-Host "✓ Vercel CLI: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: Vercel CLI未安装" -ForegroundColor Red
    Write-Host "请运行: npm install -g vercel" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "开始部署" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "请按照提示回答:" -ForegroundColor Yellow
Write-Host "1. Set up and deploy? → Y" -ForegroundColor White
Write-Host "2. Which scope? → 直接回车" -ForegroundColor White
Write-Host "3. Link to existing project? → N" -ForegroundColor White
Write-Host "4. What's your project's name? → my-space-frontend" -ForegroundColor White
Write-Host "5. In which directory is your code located? → 直接回车" -ForegroundColor White
Write-Host "6. Want to override the settings? → N" -ForegroundColor White
Write-Host ""

# 执行部署
vercel --prod

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "部署完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
