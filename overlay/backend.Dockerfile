# 学マス扩展包的后端镜像：拿 eidolon-sc 的 backend/ 源码（构建上下文 upstream），打上
# patches/backend.json 再构建。原仓库的文件不会被改动。
# 第二段照抄原项目 backend/Dockerfile 的构建步骤；原 Dockerfile 变了时 apply_patches.py 会
# 拒绝构建（见 upstream.lock），请对照更新这里。

FROM python:3.11-slim AS patched
COPY apply_patches.py upstream.lock /overlay/
COPY patches/backend.json /overlay/
COPY --from=upstream . /src
RUN rm -rf /src/.venv /src/data && \
    python /overlay/apply_patches.py /src /overlay/backend.json --lock /overlay/upstream.lock

FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app
COPY --from=patched /src/pyproject.toml /src/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY --from=patched /src/src ./src
RUN uv sync --frozen --no-dev
COPY --from=patched /src/eval ./eval

ENV PATH=/app/.venv/bin:$PATH \
    EIDOLON_DATABASE_PATH=/data/eidolon.db \
    EIDOLON_CHARACTERS_PATH=/characters/characters.toml \
    EIDOLON_STORY_PATH=/corpus/story \
    EIDOLON_GAME_CATALOG_PATH=/corpus/game/catalog.json \
    EIDOLON_MIRROR_CACHE_PATH=/data/mirror \
    EIDOLON_EVENT_NAMES_PATH=/deploy/event-names.toml
EXPOSE 8000
CMD ["eidolon"]
