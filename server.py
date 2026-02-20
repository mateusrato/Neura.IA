from flask import Flask, request, jsonify
from flask_cors import CORS

from mind import atualizar_estado, decidir_resposta

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mensagem = data.get("mensagem", "").strip()

    if not mensagem:
        return jsonify({"resposta": "Fala algo aí, Mestre."})

    # 🔥 ATUALIZA O CÉREBRO
    atualizar_estado(mensagem)

    # 🧠 NEURA DECIDE O QUE RESPONDER
    resposta = decidir_resposta(mensagem)

    return jsonify({"resposta": resposta})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)



