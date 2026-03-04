# Vercel API 测试脚本 (PowerShell版本)
# 使用方法: .\test_vercel_api.ps1

$BASE_URL = "https://my-space-beryl.vercel.app"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Vercel API 测试脚本" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 测试1: 根路径
Write-Host "测试1: 根路径 /" -ForegroundColor Yellow
Write-Host "----------------------------------------"
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/" -Method Get
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "错误: $_" -ForegroundColor Red
}
Write-Host ""
Write-Host ""

# 测试2: 健康检查
Write-Host "测试2: 健康检查 /api/health" -ForegroundColor Yellow
Write-Host "----------------------------------------"
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/api/health" -Method Get
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "错误: $_" -ForegroundColor Red
}
Write-Host ""
Write-Host ""

# 测试3: 环境变量测试
Write-Host "测试3: 环境变量 /api/test" -ForegroundColor Yellow
Write-Host "----------------------------------------"
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/api/test" -Method Get
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "错误: $_" -ForegroundColor Red
}
Write-Host ""
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "测试完成" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "如果所有测试都返回正确的JSON，说明API部署成功！" -ForegroundColor Green
Write-Host ""
Write-Host "下一步："
Write-Host "1. 如果看到错误，请查看 VERCEL_DEBUG_GUIDE.md"
Write-Host "2. 如果一切正常，可以测试上传简历功能"
Write-Host ""
