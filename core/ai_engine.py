import os
import requests
import json

class OllamaEngine:
    """
    Classe para realizar as chamadas à API local do Ollama para geração de texto.
    """
    
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model_name = os.getenv("MODEL_NAME", "llama3")
        
        if not self.base_url.endswith("/api/generate"):
            self.api_url = f"{self.base_url.rstrip('/')}/api/generate"
        else:
            self.api_url = self.base_url

    def generate_report(self, prompt: str) -> str:
        """
        Envia um prompt para o modelo Ollama e retorna a resposta gerada.
        
        Args:
            prompt (str): O super prompt preparado pelo processor.
            
        Returns:
            str: Resposta textual do modelo.
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False  # Para simplificar, desativamos o streaming de resposta
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=120)
            response.raise_for_status()
            
            data = response.json()
            return data.get("response", "Erro: O modelo não retornou a chave 'response'.")
            
        except requests.exceptions.RequestException as e:
            return f"Erro ao acessar API do Ollama: {str(e)}"
