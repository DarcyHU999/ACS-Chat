#!/bin/bash

echo "🔒 Starting Secure Deployment..."

# 1. Check environment configuration
if [ ! -f "be/.env" ]; then
    echo "❌ Error: be/.env file does not exist"
    echo "Please copy be/env.example to be/.env and configure real API keys"
    exit 1
fi

# 2. Check if API keys are configured
if grep -q "your_openai_api_key_here" be/.env; then
    echo "⚠️  Warning: Default API key detected, please configure real keys"
    echo "Edit be/.env file and set OPENAI_API_KEY"
    exit 1
fi

# 3. Set secure file permissions
chmod 600 be/.env
echo "✅ Set environment file permissions"

# 4. Clean up existing services
echo "🧹 Cleaning up existing services..."
docker compose down 2>/dev/null || true

# 5. Build secure images
echo "🏗️  Building services..."
docker compose build

# 6. Start securely configured services
echo "🚀 Starting secure services..."
docker compose up -d

# 7. Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# 8. Check service status
echo "🔍 Checking service status..."
docker compose ps

# 9. Display access information
echo ""
echo "🎉 Deployment completed!"
echo ""
echo "Access URLs:"
echo "  Frontend: http://3.27.117.234"
echo "  (Backend API protected via nginx proxy)"
echo ""
echo "Security Features:"
echo "  ✅ API restricted to specific domains"
echo "  ✅ Database local access only"
echo "  ✅ API rate limiting"
echo "  ✅ Debug mode disabled"
echo ""
echo "⚠️  Important Reminders:"
echo "  1. Close public access to ports 3000, 6333, 8000 in AWS Security Groups"
echo "  2. Regularly monitor OpenAI API usage"
echo "  3. Consider configuring SSL certificates"
echo ""

# 10. Display logs
echo "📋 Real-time logs (Ctrl+C to exit):"
docker compose logs -f 