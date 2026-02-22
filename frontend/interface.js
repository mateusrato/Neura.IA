async function enviar() {
    const input = document.getElementById("textInput");
    const texto = input.value.trim();
    if (!texto) return;

    adicionarMensagem(texto, "user");
    input.value = "";

    const res = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mensagem: texto })
    });

    const data = await res.json();
    adicionarMensagem(data.resposta, "neura");
}

function adicionarMensagem(texto, tipo) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.className = `msg ${tipo}`;
    div.innerText = texto;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}


