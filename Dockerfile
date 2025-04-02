 FROM python:3.12

# Add uv Modules
COPY --from=ghcr.io/astral-sh/uv:0.6.7 /uv /uvx /bin/

# Install dependencies
COPY ./dist/revi_toolbox-0.1.0-py3-none-any.whl /whl/

WORKDIR /app
RUN uv venv \
    && uv pip install revi_toolbox@/whl/revi_toolbox-0.1.0-py3-none-any.whl
ENV PATH="/app/.venv/bin:$PATH"
