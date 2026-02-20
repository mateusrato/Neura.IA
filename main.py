from mind import mind, atualizar_estado, decidir_resposta

print("Neura online. Digite 'sair' para encerrar.")

while True:
    user_input = input("Você: ")

    if user_input.lower() == "sair":
        print("Neura: desligando...")
        break

    # Atualiza mente da Neura
    atualizar_estado(user_input)

    # Decide o que responder
    resposta = decidir_resposta(user_input)

    print("Neura:", resposta)


