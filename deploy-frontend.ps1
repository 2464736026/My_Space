# 前端部署脚本
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "前端部署到Vercel" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否在正确的目录
$currentDir = Get-Location
Write-Host "当前目录: $currentDir" -ForegroundColor Yellow

# 检查frontend目录
if (Test-Path "frontend") {
    Write-Host "✓ frontend目录存在" -ForegroundColor Green
} else {
    Write-Host "✗ frontend目录不存在！" -ForegroundColor Red
    Write-Host "请确保在项目根目录 (E:\newP) 运行此脚本" -ForegroundColor Red
    exit 1
}

# 进入frontend目录
Write-Host "`n进入frontend目录..." -ForegroundColor Yellow
Set-Location frontend

# 检查package.json
if (Test-Path "package.json") {
    Write-Host "✓ package.json存在" -ForegroundColor Green
} else {
    Write-Host "✗ package.json不存在！" -ForegroundColor Red
    exit 1
}

# 显示当前目录
Write-Host "`n当前目录: $(Get-Location)" -ForegroundColor Yellow

# 提示用户
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "准备部署到Vercel" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "即将执行: vercel --prod" -ForegroundColor Yellow
Write-Host ""
Write-Host "按提示操作:" -ForegroundColor Green
Write-Host "1. Set up and deploy? → Y" -ForegroundColor White
Write-Host "2. Which scope? → 选择你的账号（直接回车）" -ForegroundColor White
Write-Host "3. Link to existing project? → N（创建新项目）" -ForegroundColor White
Write-Host "4. What's your project's name? → my-space-frontend" -ForegroundColor White
Write-Host "5. In which directory is your code located? → 直接回车（./）" -ForegroundColor White
Write-Host "6. Want to override the settings? → N" -ForegroundColor White
Write-Host ""

# 执行部署
Write-Host "开始部署..." -ForegroundColor Green
Write-Host ""
vercel --prod
