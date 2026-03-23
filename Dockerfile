FROM python:3.11-slim-bookworm AS builder

# Instala o uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configurações do ambiente para que o uv instale pacotes no sistema e não exija venv
ENV UV_SYSTEM_PYTHON=1
ENV UV_PROJECT_ENVIRONMENT=/usr/local

WORKDIR /app

# Copia arquivos de configuração primeiro para aproveitar cache do Docker
COPY pyproject.toml uv.lock ./

# Instala as dependências do projeto
RUN uv sync --frozen --no-dev --no-install-project

# Copia o código do projeto em si
COPY core/ core/
COPY main.py .

# Garante a existência da pasta de reports
RUN mkdir -p reports

# Ponto de entrada a ser rodado pelo container
CMD ["python", "main.py"]
