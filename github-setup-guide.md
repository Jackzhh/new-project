# GitHub 代码管理设置指南

## 🚀 **快速开始**

### 1. 创建 GitHub 仓库
```bash
# 方法一：使用 GitHub CLI (推荐)
gh repo create new-project --public --description "MCP PostgreSQL project with Docker deployment"

# 方法二：手动创建
# 访问 https://github.com/new
# 仓库名: new-project
# 描述: MCP PostgreSQL project with Docker deployment
```

### 2. 连接本地仓库到 GitHub
```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/new-project.git

# 推送代码
git branch -M main
git push -u origin main
```

## 📋 **当前项目状态**

✅ **已完成:**
- Git 仓库初始化
- 初始代码提交
- GitHub Actions 工作流创建

📁 **项目结构:**
```
new-project/
├── .github/workflows/deploy.yml  # 自动化部署
├── .dockerignore                 # Docker 忽略文件
├── .gitignore                   # Git 忽略文件
├── Dockerfile                   # Docker 镜像配置
├── README.md                    # 项目说明
├── docker-compose.yml           # Docker 编排
├── mcp-config.json             # MCP 服务配置
├── nginx.conf                  # Nginx 配置
├── react-nas-deployment-guide.md # 部署指南
├── test-docker-postgres.py     # Docker 数据库测试
└── test-mcp-postgres.py        # 本地数据库测试
```

## 🔧 **GitHub 功能配置**

### 分支保护规则
```bash
# 设置主分支保护
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["build-and-deploy"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null
```

### Issue 模板
创建 `.github/ISSUE_TEMPLATE/bug_report.md`:
```markdown
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**描述 bug**
简洁明了地描述这个 bug。

**重现步骤**
1. 进入 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

**预期行为**
简洁明了地描述你期望发生什么。

**环境信息:**
 - OS: [e.g. macOS]
 - Docker 版本: [e.g. 20.10.8]
 - Node.js 版本: [e.g. 18.0.0]
```

## 🤖 **GitHub Actions 自动化**

### 当前工作流功能:
- ✅ 代码检出
- ✅ Node.js 环境设置
- ✅ 依赖安装
- ✅ React 应用构建
- ✅ Docker 镜像构建
- ✅ 镜像保存和上传

### 扩展功能 (可选):
```yaml
# 添加代码质量检查
- name: Run ESLint
  run: npm run lint

# 添加测试
- name: Run tests
  run: npm test

# 添加安全扫描
- name: Run security audit
  run: npm audit
```

## 📊 **项目管理功能**

### 1. GitHub Projects
```bash
# 创建项目看板
gh project create --title "MCP Project Board" --body "Track development progress"
```

### 2. 里程碑管理
```bash
# 创建里程碑
gh api repos/:owner/:repo/milestones \
  --method POST \
  --field title="v1.0.0 - Initial Release" \
  --field description="First stable release with MCP PostgreSQL integration"
```

### 3. 标签管理
```bash
# 创建标签
gh label create "enhancement" --color "a2eeef" --description "New feature or request"
gh label create "bug" --color "d73a4a" --description "Something isn't working"
gh label create "documentation" --color "0075ca" --description "Improvements or additions to documentation"
```

## 🔒 **安全配置**

### 1. Secrets 管理
```bash
# 添加部署密钥
gh secret set NAS_HOST --body "your-nas-ip"
gh secret set NAS_USER --body "admin"
gh secret set NAS_SSH_KEY --body "$(cat ~/.ssh/id_rsa)"
```

### 2. Dependabot 配置
创建 `.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/.github/workflows"
    schedule:
      interval: "weekly"
```

## 🚀 **部署集成**

### 更新部署工作流
```yaml
# 在 .github/workflows/deploy.yml 中添加实际部署步骤
- name: Deploy to NAS
  if: github.ref == 'refs/heads/main'
  run: |
    # 传输镜像到 NAS
    scp app.tar ${{ secrets.NAS_USER }}@${{ secrets.NAS_HOST }}:/tmp/
    
    # SSH 到 NAS 部署
    ssh ${{ secrets.NAS_USER }}@${{ secrets.NAS_HOST }} << 'EOF'
      cd /volume1/docker/apps/
      docker stop new-project || true
      docker rm new-project || true
      docker load < /tmp/app.tar
      docker run -d --name new-project -p 3000:80 --restart unless-stopped new-project:latest
      rm /tmp/app.tar
    EOF
```

## 📝 **使用建议**

1. **定期提交**: 小步快跑，频繁提交代码
2. **分支策略**: 使用 feature 分支开发新功能
3. **代码审查**: 通过 Pull Request 进行代码审查
4. **自动化测试**: 在 CI/CD 中集成测试
5. **文档更新**: 保持 README 和文档的更新
6. **版本标签**: 使用 Git 标签标记重要版本

## 🔗 **相关链接**

- [GitHub CLI 文档](https://cli.github.com/manual/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Docker Hub](https://hub.docker.com/)
- [Dependabot 文档](https://docs.github.com/en/code-security/dependabot)
