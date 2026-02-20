history = []

def remember(user_input, response):
    history.append({
        "user": user_input,
        "neura": response
    })

def get_memory():
    return history
