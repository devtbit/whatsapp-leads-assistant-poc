import os

from flask import Flask, request

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


# Twilio setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_bot_no = os.getenv("WHATSAPP_BOT_NO")

client = Client(account_sid, auth_token)

# Flask setup
app = Flask(__name__)


def load_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    return content


@tool
def capture_lead(name: str,
                 phone_number: str,
                 email: str,
                 company_name: str) -> str:
    """
    Creates a lead in Salesforce with the given information.
    """
    printf(f"creating lead in salesforce: {name}, {phone_number}, {email}, {company_name}", flush=True)  # noqa
    return '{"status": "success"}'


def init_graph():
    llm = ChatOpenAI(model="gpt-4o-mini")
    main_prompt = load_text_file("prompts/main.txt")

    tools = [
        capture_lead,
    ]

    return create_react_agent(llm,
                              tools,
                              state_modifier=main_prompt)


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

    graph = init_graph()

    response = graph.invoke(
        {"messages": [("user", message_body)]})

    print(response, flush=True)

    resp = MessagingResponse()
    resp.message(response['messages'][-1].content)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
