# =============================================================================
# TrustLine Sentinel - Node.js Express & WebSocket Backend Container
# =============================================================================
FROM node:22-alpine

WORKDIR /app

# Copy dependency definitions
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy application source code
COPY . .

# Build the production server bundle
RUN npm run build

# Create data directory for persistent SQLite storage
RUN mkdir -p /data && chown -R node:node /app /data

# Use non-root node user for container security
USER node

# Default environment configuration
ENV NODE_ENV=production \
    PORT=5001 \
    DATA_DIR=/data

EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:5001/ || exit 1

# Start Backend Server
CMD ["node", "dist/server.cjs"]
