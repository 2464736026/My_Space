#!/bin/bash

# Vercel API 测试脚本
# 使用方法: bash test_vercel_api.sh

BASE_URL="https://my-space-beryl.vercel.app"

echo "=========================================="
echo "Vercel API 测试脚本"
echo "=========================================="
echo ""

# 测试1: 根路径
echo "测试1: 根路径 /"
echo "----------------------------------------"
curl -s "$BASE_URL/" | python -m json.tool
echo ""
echo ""

# 测试2: 健康检查
echo "测试2: 健康检查 /api/health"
echo "----------------------------------------"
curl -s "$BASE_URL/api/health" | python -m json.tool
echo ""
echo ""

# 测试3: 环境变量测试
echo "测试3: 环境变量 /api/test"
echo "----------------------------------------"
curl -s "$BASE_URL/api/test" | python -m json.tool
echo ""
echo ""

echo "=========================================="
echo "测试完成"
echo "=========================================="
echo ""
echo "如果所有测试都返回正确的JSON，说明API部署成功！"
echo ""
echo "下一步："
echo "1. 如果看到错误，请查看 VERCEL_DEBUG_GUIDE.md"
echo "2. 如果一切正常，可以测试上传简历功能"
echo ""
