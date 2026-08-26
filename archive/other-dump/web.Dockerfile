# webiconocracy — React + Vite + Firebase dev server
# Build context: repo root. Run: docker compose up web
FROM node:22-alpine AS deps
WORKDIR /app
COPY --from=webapp package.json package-lock.json* ./
RUN npm install --no-audit --no-fund

FROM node:22-alpine AS dev
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
ENV HOST=0.0.0.0
EXPOSE 3000
CMD ["npm", "run", "dev"]
