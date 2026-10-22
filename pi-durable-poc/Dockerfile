# pi-durable PoC image — Pi Durable (@earendil-works/pi-durable 1.3.0) on Node 22.
# Build context = Aria repo root (aether-build-container tars the whole tree);
# paths below are relative to it.
FROM node:22-slim

WORKDIR /app
ENV NODE_ENV=production

# Verdaccio pull-through (build-cache LXC .206:4873) — direct npmjs is
# cross-border from heavy nodes. Pinned by package-lock.json (npm ci).
COPY pi-durable-poc/package.json pi-durable-poc/package-lock.json ./
RUN npm ci --omit=dev --no-audit --no-fund \
      --registry=http://192.168.69.206:4873

COPY pi-durable-poc/src ./src

CMD ["node", "src/sentinel.mjs"]
