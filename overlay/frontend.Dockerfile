# 学マス扩展包的前端镜像：拿 eidolon-sc 的 frontend/ 源码（构建上下文 upstream），打上
# patches/frontend.json 再构建。原仓库的文件不会被改动。
# 后两段照抄原项目 frontend/Dockerfile 的构建步骤；原 Dockerfile 变了时 apply_patches.py 会
# 拒绝构建（见 upstream.lock），请对照更新这里。

FROM python:3.11-slim AS patched
COPY apply_patches.py upstream.lock /overlay/
COPY patches/frontend.json /overlay/
COPY --from=upstream . /src
RUN rm -rf /src/node_modules /src/.next /src/.cache && \
    python /overlay/apply_patches.py /src /overlay/frontend.json --lock /overlay/upstream.lock

FROM node:22-alpine AS build
WORKDIR /app
COPY --from=patched /src/package.json /src/package-lock.json ./
RUN npm ci
COPY --from=patched /src/ .
RUN npm run build

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production HOSTNAME=0.0.0.0 PORT=3000
COPY --from=build /app/.next/standalone ./
COPY --from=build /app/.next/static ./.next/static
COPY --from=build /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
