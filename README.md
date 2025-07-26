# ACS Chat

一个基于 FastAPI 和 React 的聊天应用。

## 快速开始

### 方式一：Docker（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd ACS-Chat

# 启动所有服务
./start.sh
```

访问：
- 前端：http://localhost:3000
- 后端：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 方式二：本地开发

```bash
# 克隆项目
git clone <repository-url>
cd ACS-Chat

# 自动设置开发环境
./setup-dev.sh
```

然后分别启动前后端：

```bash
# 启动后端
cd be
source .venv/bin/activate
uvicorn app.main:app --reload

# 启动前端（新终端）
cd fe
npm run dev
```

## 环境要求

- Python 3.10+
- Node.js 18+
- Docker (可选)

## 项目结构

```
ACS-Chat/
├── be/                 # 后端 (FastAPI)
│   ├── app/
│   ├── requirements.txt
│   └── Dockerfile
├── fe/                 # 前端 (React + TypeScript)
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml  # Docker 编排
├── setup-dev.sh       # 开发环境设置脚本
└── start.sh           # Docker 启动脚本
```

## 环境变量

### 1. 复制环境变量模板
```bash
cp be/env.example .env
```

### 2. 配置必要的环境变量

编辑 `.env` 文件，设置以下变量：

#### 必需配置
```env
# OpenAI API 密钥（必需）
OPENAI_API_KEY=your_openai_api_key_here
```

#### 可选配置
```env
# LangSmith 配置（可选，用于调试和监控）
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=acs-chat

# 应用配置
APP_ENV=development
DEBUG=true
```

### 3. 获取 API 密钥

#### OpenAI API 密钥
1. 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 创建新的 API 密钥
3. 复制密钥到 `.env` 文件

#### LangSmith API 密钥（可选）
1. 访问 [LangSmith](https://smith.langchain.com/)
2. 注册并获取 API 密钥
3. 复制密钥到 `.env` 文件

## 开发

### 后端开发

```bash
cd be
source .venv/bin/activate
uvicorn app.main:app --reload
```

### 前端开发

```bash
cd fe
npm run dev
```

### 调试

在 Cursor/VS Code 中：
1. 设置断点
2. 按 F5 启动调试
3. 使用调试控制台

## 部署

### 使用 Docker

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 手动部署

```bash
# 后端
cd be
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 前端
cd fe
npm install
npm run build
npm install -g serve
serve -s dist -l 3000
```

## 常见问题

### 1. 虚拟环境问题
```bash
# 重新创建虚拟环境
cd be
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. 端口被占用
```bash
# 查看端口占用
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### 3. Docker 构建失败
```bash
# 清理 Docker 缓存
docker system prune -a
docker-compose build --no-cache
```

## 贡献

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License
