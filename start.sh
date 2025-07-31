#!/bin/bash

echo "Starting ACS Chat Application..."

# check Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

# check docker compose is installed
if ! docker compose version &> /dev/null; then
    echo "Error: Docker Compose is not installed"
    exit 1
fi

# build and start services
echo "Building and starting services..."
docker compose up --build -d

echo "Services started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"

echo ""
echo "To view logs:"
echo "  docker compose logs -f"
echo ""
echo "To stop services:"
echo "  docker compose down" 