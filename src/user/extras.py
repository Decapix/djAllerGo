import secrets
from django.contrib.auth import get_user_model

def send_message(phone_number, message):
    """
    Send a message to a given user. Implement the logic depending on how you wish to contact the user.
    This could be an email, SMS, push notification, etc.
    """
    # Implémenter la logique d'envoi de message ici
    # Par exemple, envoyer un SMS ou un email
    pass

def send_riddle_to_user(phone_number, question, token):
    # Envoyez la devinette et le token à l'utilisateur
    print("send_riddle_to_userrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr", phone_number, question, token)
    

def generate_temporary_token():
    return secrets.token_urlsafe(16)


