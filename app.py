import jwt
import os
import requests
import time

from flask import Flask, request

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from langchain_openai import ChatOpenAI
from langchain.tools import tool

from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


# Twilio setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_bot_no = os.getenv("WHATSAPP_BOT_NO")

client = Client(account_sid, auth_token)

# Flask setup
app = Flask(__name__)

# Langgraph Memory
memory = MemorySaver()

# Salesforce setup
sf_key_file = 'salesforce.key'
sf_consumer_key = os.environ.get('SF_CONSUMER_KEY')
sf_sub = os.environ.get('SF_USER')


def get_sf_auth_token():
    with open(sf_key_file) as fd:
        pk = fd.read()

    claim = {
        'iss': sf_consumer_key,
        'exp': int(time.time()) + 300,
        'aud': 'https://login.salesforce.com',
        'sub': sf_sub,
    }

    assertion = jwt.encode(claim,
                           pk,
                           algorithm='RS256',
                           headers={'alg': 'RS256'})

    r = requests.post('https://login.salesforce.com/services/oauth2/token',
                      data={
                          'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',  # noqa
                          'assertion': assertion,
                      })

    response = r.json()
    return (response['instance_url'], response['access_token'])


def load_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    return content


@tool
def capture_lead(first_name: str,
                 last_name: str,
                 phone_number: str,
                 email: str,
                 company_name: str) -> str:
    """
    Creates a lead in Salesforce with the given information.
    """
    base_url, token = get_sf_auth_token()
    leads_url = f"{base_url}/services/data/v62.0/sobjects/Lead"

    response = requests.post(leads_url,
                             headers={
                                 'Authorization': f"Bearer {token}",
                                 'Content-Type': 'application/json',
                             },
                             json={
                                 'FirstName': first_name,
                                 'LastName': last_name,
                                 'Phone': phone_number,
                                 'Email': email,
                                 'Company': company_name,
                             })

    return response.text


def init_graph():
    llm = ChatOpenAI(model="gpt-4o-mini")
    main_prompt = load_text_file("prompts/main.txt")

    tools = [
        capture_lead,
    ]

    return create_react_agent(llm,
                              tools,
                              checkpointer=memory,
                              state_modifier=main_prompt)


@app.route("/test-send-message", methods=['GET'])
def send_message():
    to = request.args.get("to")

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

    user_id = request.values.get("WaId")  # user's WhatsApp ID
    message_body = request.values.get("Body")  # user's input

    graph = init_graph()

    response = graph.invoke(
        {"messages": [("user", message_body)]},
        config={"configurable": {"thread_id": user_id}})

    # print(response, flush=True)

    resp = MessagingResponse()
    resp.message(response['messages'][-1].content)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
