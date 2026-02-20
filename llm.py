import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"


def gerar_resposta(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["response"].strip()
    else:
        return "Erro ao acessar o modelo local."

