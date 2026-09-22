# gallica-mcp-server — MCP server for Gallica (BnF)
# Build context: repo root. Run: docker compose up mcp
FROM node:22-alpine AS deps
WORKDIR /app
COPY --from=mcpsrc package.json package-lock.json* ./
RUN npm install --no-audit --no-fund

FROM node:22-alpine AS dev
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
CMD ["npm", "run", "dev"]
