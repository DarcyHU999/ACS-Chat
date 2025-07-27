# 使用 Node.js 18 Alpine 镜像
FROM node:18-alpine

# 添加构建参数，用于强制重新构建
ARG BUILD_DATE=unknown

# 安装系统依赖
RUN apk add --no-cache curl

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装 Python 依赖
RUN npm ci

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 安装 http-server 用于静态文件服务
RUN npm install -g http-server

# 暴露端口
EXPOSE 3000

# 启动命令 - 使用 http-server 并配置代理
CMD ["http-server", "dist", "-p", "3000", "-P", "http://backend:8000"] 