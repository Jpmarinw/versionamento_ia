class CommitProcessor:
    """
    Processador dos dados extraídos do GitHub para criar o Super Prompt e
    passar os dados limpos ao OllamaEngine.
    """
    
    def __init__(self, ai_engine):
        self.ai = ai_engine

    def clean_diff(self, raw_diff: str) -> str:
        """
        Limita o tamanho do diff para não extrapolar a janela de contexto da LLM local.
        Coleta o limite configurado pela variável de ambiente MAX_DIFF_LENGTH (padrão 2000).
        """
        import os
        max_length = int(os.getenv("MAX_DIFF_LENGTH", 2000))
        
        if len(raw_diff) > max_length:
            return raw_diff[:max_length] + "\n\n... [DIFF TRUNCADO DEVIDO AO TAMANHO]"
        return raw_diff

    def build_prompt(self, commit_message: str, diff: str) -> str:
        """
        Constrói o Super Prompt de Engenharia de Software.
        """
        return f"""Você é um Engenheiro de Software Sênior especializado em revisão de código e arquitetura.
Sua missão é gerar um relatório técnico sobre as últimas mudanças em um repositório git. 

### INFORMAÇÕES DO COMMIT:
Mensagem do Commit: {commit_message}
Diff (mudanças no código): 
```diff
{diff}
```

Escreva o relatório EXCLUSIVAMENTE em Português do Brasil seguindo ESTRITAMENTE o formato abaixo:

## Resumo Executivo
(Explique o que foi feito de forma simples, em nível macro, ideal para que um gerente de projetos ou PO entenda).

## Mudanças Técnicas
(Liste as alterações chave no código: o que mudou e por qual motivo. Seja objetivo).

## Impacto
(Explique como esta mudança beneficia o sistema, ou se corrige algum problema ou aumenta a complexidade).
"""

    def process_and_report(self, commit_message: str, raw_diff: str) -> str:
        """
        Recebe as informações brutas do commit, limpa os dados, cria o prompt e chama a LLM.
        """
        cleaned_diff = self.clean_diff(raw_diff)
        prompt = self.build_prompt(commit_message, cleaned_diff)
        
        print("Enviando dados para a inteligência artificial local processar...")
        report = self.ai.generate_report(prompt)
        return report
