# AI Commit Reporter

O **AI Commit Reporter** é uma ferramenta para gerar relatórios detalhados e legíveis sobre os commits do seu repositório Git, analisando diffs através de Inteligência Artificial Generativa baseada no modelo `llama3` rodando localmente no Ollama (ou outro modelo/provedor).

## 🚀 Tecnologias
- **Python 3.11+**
- **uv (Gerenciador de Dependências Astral)**
- **Docker & Docker Compose**
- **Ollama (IA Local)**
- **GitHub API**

## 📦 Estrutura do Projeto
```plaintext
ai-commit-reporter/
├── core/                   # Lógica e Integração
│   ├── ai_engine.py        # Orquestração do Ollama
│   ├── git_provider.py     # Autenticação e extração via GitHub API
│   ├── processor.py        # Limpeza do diff e Engenharia de Prompt
│   └── __init__.py
├── reports/                # Relatórios Markdown gerados
├── main.py                 # Ponto de Partida
├── Dockerfile              # Docker Container Otimizado
├── docker-compose.yml      # Docker Compose local
├── .env.example            # Exemplo de ambiente
└── pyproject.toml / uv.lock # Lockfiles do projeto
```

## ⚙️ Configuração Inicial
1. **Instale as dependências (ambiente host):**
   ```bash
   uv sync
   ```
2. **Configure o `.env` do seu projeto:**
   - Faça uma cópia do arquivo `.env.example`:
   ```bash
   cp .env.example .env
   ```
   - Preencha com as suas informações:
     - `GITHUB_TOKEN`: Gerado em *Developer Settings -> Personal Access Tokens* (Classic) no GitHub, certificando de marcar o escopo `repo`.
     - `GITHUB_USER` e `GITHUB_REPO`: Seu usuário e o repositório que deseja relatar.
     - `OLLAMA_BASE_URL` e `MODEL_NAME`: Endereço em que sua conta Ollama escuta e qual modelo utilizar.

## 🧑‍💻 Testando Localmente
Subindo seu Ollama (Host) e rodando na sua máquina host:
```bash
python main.py
```
*(Verifique se o Ollama está rodando localmente o modelo llama3)*

## 🐳 Executando via Docker
Caso deseje executar de maneira isolada através dos containers:
```bash
docker compose up --build
```

Os relatórios gerados a partir do commit ficarão salvos na sua pasta `/reports` do sistema Host (já que mapeamos ela como um volume no Compose).
