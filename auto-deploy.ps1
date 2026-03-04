# 自动部署脚本
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "前端自动部署到Vercel" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 进入frontend目录
Set-Location frontend

Write-Host "当前目录: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# 创建vercel.json配置文件（如果不存在）
$vercelConfig = @"
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "framework": "vite",
  "devCommand": "npm run dev"
}
"@

if (-not (Test-Path "vercel.json")) {
    Write-Host "创建vercel.json配置..." -ForegroundColor Yellow
    $vercelConfig | Out-File -FilePath "vercel.json" -Encoding UTF8
    Write-Host "✓ 配置文件已创建" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "准备部署" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "即将执行部署命令..." -ForegroundColor Yellow
Write-Host ""
Write-Host "请按照以下提示回答:" -ForegroundColor Green
Write-Host "1. Set up and deploy? → 输入 Y" -ForegroundColor White
Write-Host "2. Which scope? → 直接回车" -ForegroundColor White
Write-Host "3. Link to existing project? → 输入 N" -ForegroundColor White
Write-Host "4. What's your project's name? → 输入 my-space-frontend" -ForegroundColor White
Write-Host "5. In which directory is your code located? → 直接回车" -ForegroundColor White
Write-Host "6. Want to override the settings? → 输入 N" -ForegroundColor White
Write-Host ""
Write-Host "按任意键开始部署..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Write-Host ""

# 执行部署
vercel --prod
