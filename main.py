import os
import datetime
from dotenv import load_dotenv

from core.git_provider import GitHubProvider
from core.ai_engine import OllamaEngine
from core.processor import CommitProcessor

def main():
    # Carrega as variáveis do arquivo .env
    load_dotenv()
    
    print("Iniciando o AI Commit Reporter...")
    
    # Validação simples
    if not os.getenv("GITHUB_TOKEN"):
        print("ERRO: O GITHUB_TOKEN não está definido. Verifique o arquivo .env.")
        return

    try:
        # 1. Recupera as informações do Git
        print(f"1/3 -> Conectando ao repositório GitHub ({os.getenv('GITHUB_USER')}/{os.getenv('GITHUB_REPO')})...")
        git = GitHubProvider()
        sha, message, author, date = git.get_latest_commit()
        
        print(f"Commit encontrado: {sha[:7]} - {message}")
        
        print("Obtendo diff das mudanças...")
        diff = git.get_commit_diff(sha)
        
        # 2. Configura a Inteligência Artificial e o Processador
        print("2/3 -> Preparando envio para o LLM Local (Ollama)...")
        ai = OllamaEngine()
        processor = CommitProcessor(ai)
        
        # 3. Processa e Gera o Relatório
        print("3/3 -> Analisando contexto de código (isso pode demorar).")
        report = processor.process_and_report(message, diff)
        
        # Salva o relatório num arquivo .md dentro da pasta reports
        save_report(sha, report, author, date)

    except Exception as e:
        print(f"Ocorreu um erro na execução: {e}")

def save_report(sha: str, report: str, author: str, date_str: str):
    if not os.path.exists("reports"):
        os.makedirs("reports")
        
    try:
        dt_utc = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        tz_offset = int(os.getenv("TIMEZONE_OFFSET", "-4")) # Fuso de Manaus por padrão
        dt_local = dt_utc + datetime.timedelta(hours=tz_offset)
        # Formata o fuso para ficar explícito na string (ex: UTC-4)
        formatted_date = dt_local.strftime(f"%d/%m/%Y às %H:%M:%S (UTC{tz_offset:+d})")
    except ValueError:
        formatted_date = date_str
        
    data_atual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"reports/commit_{sha[:7]}_{data_atual}.md"
    
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"# Relatório de Análise Automática - {sha[:7]}\n\n")
        file.write(f"**Autor do Commit:** {author}\n")
        file.write(f"**Data do Commit:** {formatted_date}\n\n")
        file.write("---\n\n")
        file.write(report)
        
    print(f"\n[SUCESSO] Relatório gerado com sucesso!\nCaminho: {file_name}")

if __name__ == "__main__":
    main()
