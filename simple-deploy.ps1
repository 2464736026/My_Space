# 简化部署脚本
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Vercel 前端部署" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查当前目录
$currentDir = Get-Location
Write-Host "当前目录: $currentDir" -ForegroundColor Yellow

# 检查是否在项目根目录
if (-not (Test-Path "frontend")) {
    Write-Host "错误: 请在项目根目录 (E:\newP) 运行此脚本" -ForegroundColor Red
    exit 1
}

# 进入frontend目录
Write-Host "进入frontend目录..." -ForegroundColor Yellow
Set-Location frontend

# 显示当前目录
Write-Host "当前目录: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# 检查必要文件
if (-not (Test-Path "package.json")) {
    Write-Host "错误: package.json 不存在!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ package.json 存在" -ForegroundColor Green
Write-Host ""

# 删除旧的.vercel配置
if (Test-Path ".vercel") {
    Write-Host "删除旧的.vercel配置..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .vercel
    Write-Host "✓ 已删除" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "开始部署到Vercel" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 执行部署
Write-Host "执行: vercel --prod" -ForegroundColor Yellow
Write-Host ""
vercel --prod

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "部署完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
