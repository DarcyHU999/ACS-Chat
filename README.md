# ACS Chat

A chat application based on FastAPI, LangChain, Qdrant vector database and React with TypeScript.

## Features

- 🤖 **AI-Powered Chat**: Powered by OpenAI GPT-4o-mini
- 🔍 **Semantic Search**: Vector-based document retrieval using Qdrant Cloud
- 📚 **Knowledge Base**: 31,000+ documents for comprehensive answers
- 🚀 **Modern Stack**: FastAPI + React + TypeScript + Docker
- 🔒 **Secure**: Production-ready with HTTPS and security configurations
- 📊 **Monitoring**: LangSmith integration for debugging and monitoring
- 💾 **Log Management**: Optimized for small instances (t3a.nano)
- ☁️ **Cloud Infrastructure**: Qdrant Cloud for better performance and cost optimization

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Nginx     │    │  Frontend   │    │   Backend   │    │ Qdrant Cloud│
│ (Port 80/443)│◄──►│  (Port 3000)│◄──►│  (Port 8000)│◄──►│  (Cloud API)│
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                            │
                                            └──► OpenAI API
```

## Quick Start

### Method 1: Docker (Recommended)

```bash
# Clone the project
git clone <repository-url>
cd ACS-Chat

# Start all services
./start.sh
```

**Access URLs:**
- **Frontend**: https://acschat.cc (HTTPS)
- **Backend API**: https://acschat.cc/api/v1/
- **API Documentation**: https://acschat.cc/docs (disabled in production)

### Method 2: Local Development

```bash
# Clone the project
git clone <repository-url>
cd ACS-Chat

# Auto-setup development environment
./setup-dev.sh
```

Then start frontend and backend separately:

```bash
# Start backend
cd be
source .venv/bin/activate
uvicorn app.main:app --reload

# Start frontend (new terminal)
cd fe
npm run dev
```

## Requirements

- **Python**: 3.10+
- **Node.js**: 18+
- **Docker**: 20.10+ (for Docker deployment)
- **OpenAI API Key**: Required for AI functionality

## Project Structure

```
ACS-Chat/
├── be/                          # Backend (FastAPI + LangChain)
│   ├── app/
│   │   ├── api/                 # API routes
│   │   ├── chains/              # LangChain QA chains
│   │   ├── config/              # Configuration files
│   │   ├── middleware/          # Custom middleware
│   │   ├── services/            # Business logic services
│   │   └── util/                # Utility functions
│   ├── requirements.txt
│   └── Dockerfile
├── fe/                          # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   └── theme/               # UI theme
│   ├── package.json
│   └── Dockerfile
├── nginx.conf                   # Nginx reverse proxy config
├── docker-compose.yml           # Docker orchestration
├── nginx.conf                   # Nginx reverse proxy config
├── setup-dev.sh                 # Development setup script
├── start.sh                     # Docker startup script
├── check-security.sh            # Security check script
├── deploy-secure.sh             # Secure deployment script
├── manage-logs.sh               # Log management script
└── security-checklist.md        # Security guidelines
```

## Environment Variables

### 1. Copy environment variable template
```bash
cp be/env.example be/.env
```

### 2. Configure environment variables

Edit `be/.env` file:

#### Required Configuration
```env
# OpenAI API Key (Required)
OPENAI_API_KEY=your_openai_api_key_here
```

#### Optional Configuration
```env
# LangSmith Configuration (Optional, for debugging and monitoring)
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=acs-chat
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Qdrant Cloud Configuration (Production)
QDRANT_URL=https://your-cluster.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here

# Local Qdrant Configuration (Development)
# QDRANT_HOST=localhost
```

### 3. Get API Keys

#### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key to `be/.env`

#### LangSmith API Key (Optional)
1. Visit [LangSmith](https://smith.langchain.com/)
2. Register and get an API key
3. Copy the key to `be/.env`

## Development

### Backend Development

```bash
cd be
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd fe
npm run dev
```

### Vector Database

The application uses Qdrant Cloud vector database with 31,000+ documents:

```bash
# Check vector database status
docker compose exec backend python -c "
from app.services.vectorstore import get_vectorstore
print('Vector database ready:', get_vectorstore() is not None)
"

# Check Qdrant Cloud connection
docker compose exec backend python -c "
from qdrant_client import QdrantClient
import os
client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))
info = client.get_collection('ACS-Chat')
print(f'Data points: {info.points_count}')
"
```

## Infrastructure Migration

### Qdrant Cloud Migration

The application has been migrated from local Qdrant to Qdrant Cloud for better performance and cost optimization:

#### Benefits
- ✅ **Cost Reduction**: No local database storage and maintenance
- ✅ **Better Performance**: Cloud-optimized infrastructure
- ✅ **Scalability**: Automatic scaling with usage
- ✅ **Reliability**: 99.9% uptime guarantee
- ✅ **Security**: Enterprise-grade security

#### Migration Details
- **Data Points**: 31,091 documents migrated
- **Vector Dimension**: 1536
- **Collection Name**: ACS-Chat
- **Connection**: HTTPS with API key authentication

#### Configuration
```env
# Qdrant Cloud Configuration
QDRANT_URL=https://your-cluster.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here
```

### Instance Optimization

The application is now optimized for **t3a.nano** instances:

#### Memory Usage (Optimized)
- **Backend**: 123MB
- **Frontend**: 25MB
- **Nginx**: 8MB
- **Docker**: 63MB
- **System**: 50MB
- **Total**: ~269MB < 512MB (t3a.nano limit)

#### Cost Savings
- **Before**: t3.small ($20/month) + local Qdrant
- **After**: t3a.nano ($3.5/month) + Qdrant Cloud (free tier)
- **Monthly Savings**: $16.5
- **Annual Savings**: $198

## Deployment

```bash
# Secure deployment (recommended)
./deploy-secure.sh

# Or manual deployment
docker compose up -d
```

### Manual Deployment

```bash
# Backend
cd be
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd fe
npm install
npm run build
npm install -g serve
serve -s dist -l 3000
```

### Security Features

- ✅ **CORS Protection**: Restricted to specific domains
- ✅ **Rate Limiting**: API rate limiting (10 req/s)
- ✅ **Network Security**: Database and API ports local-only
- ✅ **Production Hardening**: Debug mode disabled
- ✅ **Reverse Proxy**: Nginx with security headers

## Log Management (Optimized for t3a.nano)

### Automatic Log Management
The application includes optimized log management for small instances:

```bash
# Check disk usage and log statistics
./manage-logs.sh usage

# View log statistics
./manage-logs.sh stats

# Clean old logs manually
./manage-logs.sh clean

# Configure log rotation
./manage-logs.sh configure
```

### Log Configuration
- **Docker Logs**: Limited to 10MB per container, max 3 files
- **Qdrant Logs**: Limited to 20MB, max 5 files
- **Auto Cleanup**: Daily at 2:00 AM via cron job
- **System Logs**: 7-day retention with compression

### Disk Space Optimization
```bash
# Monitor disk usage
df -h /

# Check Docker log sizes
sudo du -sh /var/lib/docker/containers/*/logs

# Clean up old logs immediately
./manage-logs.sh clean
```

## Monitoring and Debugging

### Check Service Status
```bash
# View all services
docker compose ps

# Check logs
docker compose logs -f

# Security check
./check-security.sh
```

### LangSmith Integration
- Enable tracing for debugging
- Monitor API usage and performance
- Track conversation flows

## Common Issues

### 1. Environment Setup
```bash
# Recreate virtual environment
cd be
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Port Conflicts
```bash
# Check and kill processes
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### 3. Docker Issues
```bash
# Clean and rebuild
docker system prune -a
docker compose build --no-cache
docker compose up -d
```

### 4. Vector Database Issues
```bash
# Check Qdrant Cloud connection
docker compose exec backend python -c "
from qdrant_client import QdrantClient
import os
try:
    client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))
    info = client.get_collection('ACS-Chat')
    print(f'Qdrant Cloud connected, data points: {info.points_count}')
except Exception as e:
    print(f'Qdrant Cloud connection failed: {e}')
"
```

### 5. Disk Space Issues
```bash
# Check disk usage
./manage-logs.sh usage

# Clean logs
./manage-logs.sh clean

# Remove unused Docker resources
docker system prune -f
```

## Security Checklist

- [ ] Set secure file permissions: `chmod 600 be/.env`
- [ ] Configure AWS Security Groups (close ports 3000, 8000)
- [ ] Set OpenAI API usage limits
- [ ] Enable SSL/HTTPS ✅ (Configured)
- [ ] Regular security updates
- [ ] Monitor disk usage and logs
- [ ] Configure Qdrant Cloud API key ✅ (Configured)
- [ ] Enable HSTS headers ✅ (Configured)

See `security-checklist.md` for detailed security guidelines.

## Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details.
