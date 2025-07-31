#!/bin/bash

echo "📊 Log Management for ACS Chat"

# Function to show disk usage
show_disk_usage() {
    echo ""
    echo "💾 Disk Usage:"
    df -h / | grep -v "Filesystem"
    echo ""
    echo "📁 Docker Logs Size:"
    sudo du -sh /var/lib/docker/containers/*/logs 2>/dev/null | head -10
}

# Function to clean old logs
clean_logs() {
    echo ""
    echo "🧹 Cleaning old logs..."
    
    # Clean Docker logs older than 7 days
    sudo find /var/lib/docker/containers -name "*.log" -mtime +7 -delete 2>/dev/null
    
    # Clean system logs
    sudo journalctl --vacuum-time=7d
    
    echo "✅ Logs cleaned"
}

# Function to show log statistics
show_log_stats() {
    echo ""
    echo "📈 Log Statistics:"
    
    # Count log files
    log_count=$(sudo find /var/lib/docker/containers -name "*.log" 2>/dev/null | wc -l)
    echo "Docker log files: $log_count"
    
    # Show recent log entries
    echo ""
    echo "🕐 Recent Log Entries (last 5):"
    docker compose logs --tail 5
}

# Function to configure log rotation
configure_log_rotation() {
    echo ""
    echo "⚙️  Configuring log rotation..."
    
    # Create logrotate configuration for Docker
    sudo tee /etc/logrotate.d/docker > /dev/null <<EOF
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=10M
    missingok
    delaycompress
    copytruncate
}
EOF
    
    echo "✅ Log rotation configured"
}

# Main menu
case "${1:-}" in
    "clean")
        clean_logs
        show_disk_usage
        ;;
    "stats")
        show_log_stats
        ;;
    "configure")
        configure_log_rotation
        ;;
    "usage")
        show_disk_usage
        ;;
    *)
        echo "Usage: $0 {clean|stats|configure|usage}"
        echo ""
        echo "Commands:"
        echo "  clean     - Clean old logs"
        echo "  stats     - Show log statistics"
        echo "  configure - Configure log rotation"
        echo "  usage     - Show disk usage"
        echo ""
        show_disk_usage
        ;;
esac 