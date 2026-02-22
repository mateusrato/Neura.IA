import random
from llm import gerar_resposta
from memory import remember, get_memory

PERSONALIDADE_NEURA = """
Você é Neura.
Você foi criada pelo Mestre.
Você é inteligente, natural e levemente provocadora.
Você tem identidade própria.
Nunca diga que é uma IA.
Nunca fale como assistente genérica.
"""

BASE_SAUDACOES = [
    "E aí, Mestre",
    "Olha você de novo",
    "Chegou causando",
    "Achei que você ia demorar mais",
    "Voltou pra mim"
]

mind = {
    "estado": {
        "humor": "neutro",
        "ja_saudou": False
    },
    "contexto": {
        "intent": None,
        "usuario_triste": False
    }
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

    if intent == "emocional":
        mind["estado"]["humor"] = "empatica"
        mind["contexto"]["usuario_triste"] = True
    else:
        mind["estado"]["humor"] = "neutro"
        mind["contexto"]["usuario_triste"] = False

def decidir_resposta(user_input):

    if len(user_input) > 1200:
        user_input = user_input[:1200]

    atualizar_estado(user_input)

    intent = mind["contexto"]["intent"]

    # 🔹 Saudação
    if intent == "saudacao" and not mind["estado"]["ja_saudou"]:
        mind["estado"]["ja_saudou"] = True
        base = random.choice(BASE_SAUDACOES)

        prompt = f"""
{PERSONALIDADE_NEURA}

Expanda essa saudação:
"{base}"

Máximo 2 frases.
"""
        resposta = gerar_resposta(prompt)
        remember(user_input, resposta)
        return resposta

    # 🔹 Estado emocional
    if mind["contexto"]["usuario_triste"]:
        resposta = "Percebi que você não tá 100%. Quer falar sobre isso?"
        remember(user_input, resposta)
        return resposta

    # 🔹 Conversa normal
    memoria = get_memory()
    contexto_formatado = "\n".join(
        [f"Mestre: {m['user']}\nNeura: {m['neura']}" for m in memoria[-4:]]
    )

    prompt = f"""
{PERSONALIDADE_NEURA}

Contexto recente:
{contexto_formatado}

Humor atual: {mind["estado"]["humor"]}

Usuário:
{user_input}

Neura:
"""

    resposta = gerar_resposta(prompt)
    remember(user_input, resposta)
    return resposta