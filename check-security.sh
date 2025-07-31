#!/bin/bash

echo "🔍 Security Status Check..."

# Check service running status
echo ""
echo "📊 Service Status:"
docker compose ps

# Check port binding
echo ""
echo "🌐 Port Binding Status:"
netstat -tuln | grep -E ":80|:3000|:6333|:8000" | while read line; do
    if echo "$line" | grep -q "127.0.0.1"; then
        echo "✅ $line (Secure - Local only)"
    elif echo "$line" | grep -q "0.0.0.0:80"; then
        echo "✅ $line (Normal - nginx proxy)"
    else
        echo "⚠️  $line (Warning - Public exposure)"
    fi
done

# Check .env file permissions
echo ""
echo "🔐 .env File Permissions:"
if [ -f "be/.env" ]; then
    perm=$(stat -c %a be/.env)
    if [ "$perm" = "600" ]; then
        echo "✅ be/.env permissions secure ($perm)"
    else
        echo "⚠️  be/.env permissions insecure ($perm) - Recommend setting to 600"
    fi
else
    echo "❌ be/.env file does not exist"
fi

# Check nginx status
echo ""
echo "🔄 Nginx Proxy Status:"
if curl -s -I http://localhost/api/v1/health &>/dev/null; then
    echo "✅ Nginx proxy working normally"
else
    echo "⚠️  Nginx proxy may have issues"
fi

# Display access URLs
echo ""
echo "🌍 Access URLs:"
echo "  Frontend: http://3.27.117.234"
echo "  API: http://3.27.117.234/api/"

echo ""
echo "💡 If security issues are found, run: ./deploy-secure.sh" 