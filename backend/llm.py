import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"  # escolha um modelo e mantenha padrão

def gerar_resposta(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.6,
            "num_predict": 150,
            "num_ctx": 1024,
            "top_p": 0.9,
            "top_k": 40
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()

    except requests.exceptions.Timeout:
        return "Demorei pra pensar nisso... tenta de novo."

    except Exception as e:
        print("ERRO OLLAMA:", e)
        return "Algo deu errado aqui."