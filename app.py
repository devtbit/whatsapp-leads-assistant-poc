import os

from flask import Flask, request

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from langchain_openai import ChatOpenAI


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
    # print(f"Sending message to whatsapp:+{to}", flush=True)

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
    # print(request.values, flush=True)

    # user_id = request.values.get("WaId")  # user's WhatsApp ID
    message_body = request.values.get("Body")  # user's input

    llm = ChatOpenAI(model="gpt-4o-mini")

    messages = [
        (
            "system",
            "You are a helpful assistant"
        ),
        ("human", message_body),
    ]

    response = llm.invoke(messages)
    print(response, flush=True)

    resp = MessagingResponse()
    resp.message(response.content)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
