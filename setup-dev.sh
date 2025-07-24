#!/bin/bash

echo "Setting up ACS Chat development environment..."

# check python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.10 or later"
    exit 1
fi

# check node is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    echo "Please install Node.js 18 or later"
    exit 1
fi

# setup backend
echo "Setting up backend..."
cd be

# check virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Backend setup completed!"

# setup frontend
echo "Setting up frontend..."
cd ../fe

# install node dependencies
echo "Installing Node.js dependencies..."
npm install

echo "Frontend setup completed!"

# go back to root directory
cd ..

# check environment variables file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  Environment variables file not found"
    echo "Please copy the environment template and configure:"
    echo "  cp be/env.example .env"
    echo ""
    echo "Then edit .env file and set the following variables:"
    echo "  - OPENAI_API_KEY (required)"
    echo "  - Other optional configurations"
    echo ""
    echo "Get OpenAI API key:"
    echo "  https://platform.openai.com/api-keys"
else
    echo ""
    echo "✅ Environment variables file exists"
fi

echo ""
echo "Development environment setup completed!"
echo ""
echo "To start backend:"
echo "  cd be && source .venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "To start frontend:"
echo "  cd fe && npm run dev"
echo ""
echo "To start with Docker:"
echo "  ./start.sh" 