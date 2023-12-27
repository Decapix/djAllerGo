import secrets



def send_riddle_to_user(phone_number, question, token):
    # Envoyez la devinette et le token à l'utilisateur
    print("send_riddle_to_userrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr", phone_number, question, token)
    

def generate_temporary_token():
    return secrets.token_urlsafe(16)