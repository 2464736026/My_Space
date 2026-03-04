#!/bin/bash

# AI智能简历分析系统 - 快速部署脚本

echo "=========================================="
echo "  AI智能简历分析系统 - 部署脚本"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查Git仓库
echo -e "${YELLOW}[1/5] 检查Git仓库...${NC}"
if [ ! -d ".git" ]; then
    echo -e "${RED}错误: 未找到Git仓库，请先初始化Git${NC}"
    echo "运行: git init"
    exit 1
fi
echo -e "${GREEN}✓ Git仓库已就绪${NC}"
echo ""

# 检查API密钥配置
echo -e "${YELLOW}[2/5] 检查API密钥配置...${NC}"
if grep -q "your-openai-api-key-here" backend/config.py; then
    echo -e "${RED}错误: 请先在 backend/config.py 中配置OpenAI API密钥${NC}"
    exit 1
fi
echo -e "${GREEN}✓ API密钥已配置${NC}"
echo ""

# 提交代码到GitHub
echo -e "${YELLOW}[3/5] 提交代码到GitHub...${NC}"
read -p "请输入提交信息 (默认: Update deployment): " commit_msg
commit_msg=${commit_msg:-"Update deployment"}

git add .
git commit -m "$commit_msg"

# 检查是否有远程仓库
if ! git remote | grep -q "origin"; then
    echo -e "${YELLOW}未找到远程仓库，请输入GitHub仓库地址:${NC}"
    read -p "GitHub仓库地址 (例: https://github.com/username/repo.git): " repo_url
    git remote add origin "$repo_url"
fi

git push origin main
echo -e "${GREEN}✓ 代码已推送到GitHub${NC}"
echo ""

# 部署到阿里云FC
echo -e "${YELLOW}[4/5] 部署后端到阿里云函数计算...${NC}"
echo "请确保已安装并配置 Funcraft 工具"
echo "如未安装，运行: npm install @alicloud/fun -g"
echo "如未配置，运行: fun config"
echo ""
read -p "是否继续部署到阿里云FC? (y/n): " deploy_fc

if [ "$deploy_fc" = "y" ] || [ "$deploy_fc" = "Y" ]; then
    cd backend
    fun deploy
    cd ..
    echo -e "${GREEN}✓ 后端已部署到阿里云FC${NC}"
else
    echo -e "${YELLOW}跳过阿里云FC部署${NC}"
fi
echo ""

# GitHub Pages部署提示
echo -e "${YELLOW}[5/5] GitHub Pages部署...${NC}"
echo "GitHub Actions会自动部署前端到GitHub Pages"
echo "请访问: https://github.com/你的用户名/你的仓库名/actions"
echo "查看部署进度"
echo ""
echo -e "${GREEN}部署完成后，访问以下地址:${NC}"
echo "前端: https://你的用户名.github.io/resume-analyzer/"
echo "后端: 查看阿里云FC控制台获取HTTP触发器地址"
echo ""

echo "=========================================="
echo -e "${GREEN}  部署流程完成！${NC}"
echo "=========================================="
echo ""
echo "下一步:"
echo "1. 在GitHub仓库中启用GitHub Pages (Settings → Pages)"
echo "2. 更新 frontend/src/App.jsx 中的 API_BASE_URL 为阿里云FC地址"
echo "3. 再次推送代码: git push origin main"
echo "4. 等待GitHub Actions自动部署"
echo ""
echo "详细说明请查看: DEPLOYMENT_GUIDE.md"
