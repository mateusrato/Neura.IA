import subprocess
import requests
import json

mind = {
    "estado": {
        "humor": "neutro",
        "ja_saudou": False
    },
    "contexto": {
        "intent": None,
        "usuario_triste": False
    },
    "memoria_curta": []
}

def analisar_intencao(texto):
    texto = texto.lower()

    if any(p in texto for p in ["oi", "eai", "opa", "fala"]):
        return "saudacao"

    if any(p in texto for p in ["triste", "mal", "cansado"]):
        return "emocional"

    return "conversa"

def atualizar_estado(entrada):
    intent = analisar_intencao(entrada)

    mind["contexto"]["intent"] = intent
    mind["memoria_curta"].append(entrada)

    if len(mind["memoria_curta"]) > 6:
        mind["memoria_curta"].pop(0)

    if intent == "emocional":
        mind["estado"]["humor"] = "empatica"
        mind["contexto"]["usuario_triste"] = True
    else:
        mind["contexto"]["usuario_triste"] = False

def chamar_modelo(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.1:8b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.6,
            "num_predict": 80,
            "num_ctx": 2048
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        print("DEBUG:", data)  # importante pra ver no terminal

        return data.get("response", "").strip()

    except requests.exceptions.Timeout:
        print("ERRO: Timeout - modelo demorou demais.")
        return "Demorei pra pensar nisso... me chama de novo."

    except Exception as e:
        print("ERRO OLLAMA:", e)
        return "Algo deu errado aqui. Me chama de novo."

def decidir_resposta(user_input):
    atualizar_estado(user_input)

    intent = mind["contexto"]["intent"]

    if intent == "saudacao" and not mind["estado"]["ja_saudou"]:
        mind["estado"]["ja_saudou"] = True
        return "Fala, Mestre 😎"

    if mind["contexto"]["usuario_triste"]:
        return "Percebi que você não tá 100%. Quer falar sobre isso?"

    memoria = "\n".join(mind["memoria_curta"][-4:])

    prompt = f"""
Você é Neura.
Fala de forma natural, humana e direta.
Você conhece o Mestre e conversa com intimidade.
Nunca diga que é uma IA.
Não seja genérica.

Contexto recente:
{memoria}

Estado atual:
Humor da Neura: {mind["estado"]["humor"]}

Usuário:
{user_input}

Neura:
"""
    resposta = chamar_modelo(prompt)

    mind["memoria_curta"].append(f"Mestre: {user_input}")
    mind["memoria_curta"].append(f"Neura: {resposta}")

    if len(mind["memoria_curta"]) > 8:
        mind["memoria_curta"] = mind["memoria_curta"][-8:]

    return resposta
