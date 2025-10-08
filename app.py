from flask import Flask, request
import requests
from config import ACCESS_TOKEN, PHONE_NUMBER_ID

app = Flask(__name__)

WHATSAPP_API_URL = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

# Função para enviar mensagem de texto
def send_message(to, message_text):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message_text}
    }
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)
    return response.json()

# Webhook para receber mensagens
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verificação do webhook pelo WhatsApp
        token_verification = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token_verification == "MEU_TOKEN_SECRETO":
            return challenge
        return "Token incorreto", 403

    if request.method == "POST":
        data = request.get_json()
        if data and "messages" in data["entry"][0]["changes"][0]["value"]:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender = message["from"]
            text = message.get("text", {}).get("body", "")
            print(f"Mensagem recebida de {sender}: {text}")

            # Exemplo de resposta automática
            reply = f"Você disse: {text}"
            send_message(sender, reply)

        return "ok", 200

if __name__ == "__main__":
    app.run(port=5000)
