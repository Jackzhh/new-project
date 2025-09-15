#!/bin/bash

echo "🔍 验证 GitHub 推送结果"
echo "========================"

# 检查远程仓库连接
echo "📡 检查远程仓库..."
git remote -v

# 检查推送状态
echo -e "\n📤 检查推送状态..."
git status

# 检查提交历史
echo -e "\n📝 提交历史..."
git log --oneline

# 尝试访问 GitHub 仓库
echo -e "\n🌐 检查 GitHub 仓库可访问性..."
REPO_URL="https://github.com/Jackzhh/new-project"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $REPO_URL)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ GitHub 仓库可访问: $REPO_URL"
else
    echo "❌ GitHub 仓库不可访问 (HTTP $HTTP_CODE): $REPO_URL"
    echo "请确保仓库已创建并且是 public 的"
fi

# 检查 GitHub Actions
echo -e "\n🤖 GitHub Actions 状态..."
if git ls-remote --heads origin main >/dev/null 2>&1; then
    echo "✅ 代码已推送到 GitHub"
    echo "📋 GitHub Actions 工作流应该会自动触发"
    echo "🔗 查看 Actions: $REPO_URL/actions"
else
    echo "❌ 代码尚未推送到 GitHub"
fi

echo -e "\n✨ 验证完成!"
