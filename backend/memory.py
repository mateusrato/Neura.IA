history = []

def remember(user_input, response):
    history.append({
        "user": user_input,
        "neura": response
    })

    if len(history) > 20:
        history.pop(0)

def get_memory():
    return history
