import os

from flask import Flask, request
from twilio.rest import Client


# Twilio setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_bot_no = os.getenv("WHATSAPP_BOT_NO")

client = Client(account_sid, auth_token)

# Flask setup
app = Flask(__name__)


@app.route("/test-send-message", methods=['GET'])
def send_message():
    to = request.args.get("to")
    print(f"Sending message to whatsapp:+{to}")

    message = client.messages.create(
        from_=f"whatsapp:+{whatsapp_bot_no}",
        body="Hello world!",
        to=f"whatsapp:+{to}"
    )

    return f"Message sent! {message.sid}"


@app.route("/")
def index():
    return "Hello, world!"


@app.route("/reply", methods=["POST"])
def reply():
    print(request.values, flush=True)
    return "Message received!"


if __name__ == "__main__":
    app.run(debug=True)
