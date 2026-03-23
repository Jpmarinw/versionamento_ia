# Usa uma imagem oficial do Python, otimizada e leve
FROM python:3.11-slim-bookworm AS builder

# Instala o uv (gerenciador de pacotes ultrarrápido)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configurações do ambiente para que o uv instale pacotes no sistema e não exija venv
ENV UV_SYSTEM_PYTHON=1
ENV UV_PROJECT_ENVIRONMENT=/usr/local

WORKDIR /app

# Copiar arquivos de configuração primeiro para aproveitar cache lógico do Docker
COPY pyproject.toml uv.lock ./

# Instalar as dependências do projeto (frozens) para garantir exatidão
RUN uv sync --frozen --no-dev --no-install-project

# Agora copiamos o código do projeto em si
COPY core/ core/
COPY main.py .

# Garantimos a existência da pasta de reports
RUN mkdir -p reports

# O ponto de entrada a ser rodado pelo container
CMD ["python", "main.py"]
