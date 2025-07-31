# Use Node.js 18 Alpine image
FROM node:18-alpine

# Add build argument for forcing rebuild
ARG BUILD_DATE=unknown

# Install system dependencies
RUN apk add --no-cache curl

# Set working directory
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install Python dependencies
RUN npm ci

# Copy source code
COPY . .

# Build application - multiple ways to ensure success
RUN npm run build || npx vite build

# Verify dist directory exists and contains files
RUN ls -la dist/ && [ "$(ls -A dist/)" ] && echo "✅ Build successful!" || (echo "❌ Build failed!" && exit 1)

# Install http-server for static file serving
RUN npm install -g http-server

# Expose port
EXPOSE 3000

# Start command - use http-server with proxy configuration
CMD ["http-server", "dist", "-p", "3000", "-P", "http://backend:8000", "-c", "0"] 