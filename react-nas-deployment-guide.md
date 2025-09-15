# React 应用部署到 NAS Docker 完整指南

## 📋 **部署流程概览**

```
React 开发 → 构建生产版本 → Docker 镜像 → 推送到 NAS → 运行容器
```

## 🔧 **1. React 项目准备**

### 创建 React 项目（如果还没有）
```bash
npx create-react-app my-react-app
cd my-react-app
```

### 构建生产版本
```bash
npm run build
```

## 🐳 **2. Docker 配置**

### Dockerfile
```dockerfile
# 多阶段构建
FROM node:18-alpine AS builder

# 设置工作目录
WORKDIR /app

# 复制 package 文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 生产阶段
FROM nginx:alpine

# 复制构建文件到 nginx
COPY --from=builder /app/build /usr/share/nginx/html

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 80

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"]
```

### nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        # 支持 React Router
        location / {
            try_files $uri $uri/ /index.html;
        }

        # 静态资源缓存
        location /static/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  react-app:
    build: .
    container_name: my-react-app
    ports:
      - "3000:80"
    restart: unless-stopped
    networks:
      - web

networks:
  web:
    external: true
```

### .dockerignore
```
node_modules
npm-debug.log
Dockerfile
.dockerignore
.git
.gitignore
README.md
.env
.nyc_output
coverage
.cache
```

## 🏠 **3. NAS 服务器准备**

### 确保 NAS 支持 Docker
```bash
# SSH 连接到 NAS
ssh admin@your-nas-ip

# 检查 Docker 状态
docker --version
docker-compose --version
```

### 创建项目目录
```bash
# 在 NAS 上创建项目目录
mkdir -p /volume1/docker/react-apps/my-react-app
cd /volume1/docker/react-apps/my-react-app
```

## 🚀 **4. 部署方法**

### 方法一：直接构建部署
```bash
# 1. 将项目文件传输到 NAS
scp -r ./my-react-app admin@your-nas-ip:/volume1/docker/react-apps/

# 2. SSH 到 NAS 构建并运行
ssh admin@your-nas-ip
cd /volume1/docker/react-apps/my-react-app
docker-compose up -d --build
```

### 方法二：镜像推送部署
```bash
# 1. 本地构建镜像
docker build -t my-react-app:latest .

# 2. 保存镜像为文件
docker save my-react-app:latest > my-react-app.tar

# 3. 传输到 NAS
scp my-react-app.tar admin@your-nas-ip:/volume1/docker/images/

# 4. 在 NAS 上加载镜像
ssh admin@your-nas-ip
docker load < /volume1/docker/images/my-react-app.tar

# 5. 运行容器
docker run -d --name my-react-app -p 3000:80 my-react-app:latest
```

### 方法三：私有 Registry 部署
```bash
# 1. 在 NAS 上搭建私有 Registry
docker run -d -p 5000:5000 --name registry registry:2

# 2. 本地推送镜像
docker tag my-react-app:latest your-nas-ip:5000/my-react-app:latest
docker push your-nas-ip:5000/my-react-app:latest

# 3. NAS 拉取并运行
docker pull your-nas-ip:5000/my-react-app:latest
docker run -d --name my-react-app -p 3000:80 your-nas-ip:5000/my-react-app:latest
```

## 🔄 **5. 自动化部署脚本**

### deploy.sh
```bash
#!/bin/bash

# 配置变量
NAS_IP="your-nas-ip"
NAS_USER="admin"
APP_NAME="my-react-app"
APP_PORT="3000"
REMOTE_PATH="/volume1/docker/react-apps"

echo "🚀 开始部署 React 应用到 NAS..."

# 1. 构建 React 应用
echo "📦 构建 React 应用..."
npm run build

# 2. 构建 Docker 镜像
echo "🐳 构建 Docker 镜像..."
docker build -t $APP_NAME:latest .

# 3. 保存镜像
echo "💾 保存 Docker 镜像..."
docker save $APP_NAME:latest > $APP_NAME.tar

# 4. 传输到 NAS
echo "📤 传输镜像到 NAS..."
scp $APP_NAME.tar $NAS_USER@$NAS_IP:$REMOTE_PATH/

# 5. 在 NAS 上部署
echo "🏠 在 NAS 上部署应用..."
ssh $NAS_USER@$NAS_IP << EOF
cd $REMOTE_PATH
docker stop $APP_NAME 2>/dev/null || true
docker rm $APP_NAME 2>/dev/null || true
docker load < $APP_NAME.tar
docker run -d --name $APP_NAME -p $APP_PORT:80 --restart unless-stopped $APP_NAME:latest
rm $APP_NAME.tar
EOF

# 6. 清理本地文件
rm $APP_NAME.tar

echo "✅ 部署完成！"
echo "🌐 访问地址: http://$NAS_IP:$APP_PORT"
```

### package.json 脚本
```json
{
  "scripts": {
    "build": "react-scripts build",
    "deploy": "./deploy.sh",
    "deploy:dev": "npm run build && ./deploy.sh"
  }
}
```

## 🔧 **6. NAS 特定配置**

### Synology NAS
```bash
# 使用 Synology Docker GUI
# 1. 打开 Docker 套件
# 2. 注册表 → 搜索 nginx
# 3. 映像 → 导入本地镜像
# 4. 容器 → 创建容器
```

### QNAP NAS
```bash
# 使用 Container Station
# 1. 打开 Container Station
# 2. 创建 → 从镜像创建
# 3. 配置端口映射和卷挂载
```

## 🌐 **7. 反向代理配置**

### Nginx 反向代理
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Traefik 配置
```yaml
version: '3.8'

services:
  react-app:
    build: .
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.react-app.rule=Host(`your-domain.com`)"
      - "traefik.http.services.react-app.loadbalancer.server.port=80"
```

## 🔍 **8. 监控和维护**

### 健康检查
```dockerfile
# 在 Dockerfile 中添加
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
```

### 日志查看
```bash
# 查看容器日志
docker logs my-react-app

# 实时查看日志
docker logs -f my-react-app
```

### 更新部署
```bash
# 停止旧容器
docker stop my-react-app
docker rm my-react-app

# 运行新容器
docker run -d --name my-react-app -p 3000:80 my-react-app:latest
```

## 🛡️ **9. 安全配置**

### HTTPS 配置
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;
    
    location / {
        proxy_pass http://localhost:3000;
    }
}
```

### 防火墙配置
```bash
# 只允许特定端口访问
iptables -A INPUT -p tcp --dport 3000 -s your-allowed-ip -j ACCEPT
iptables -A INPUT -p tcp --dport 3000 -j DROP
```

## 📝 **使用建议**

1. **环境变量管理**: 使用 .env 文件管理不同环境的配置
2. **多阶段构建**: 减小镜像大小，提高安全性
3. **健康检查**: 确保应用正常运行
4. **日志管理**: 配置日志轮转，避免磁盘空间不足
5. **备份策略**: 定期备份应用数据和配置
6. **版本管理**: 使用标签管理不同版本的镜像
7. **资源限制**: 设置容器资源限制，避免影响 NAS 性能
