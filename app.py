import os

from twilio.rest import Client

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
whatsapp_author_no = os.getenv("WHATSAPP_AUTHOR_NO")
whatsapp_recv_no = os.getenv("WHATSAPP_RECV_NO")

client = Client(account_sid, auth_token)

print(f"Sending message to whatsapp:+{whatsapp_recv_no} from whatsapp:+{whatsapp_author_no}")

message = client.messages.create(
    from_=f"whatsapp:+{whatsapp_author_no}",
    body="Hello world!",
    to=f"whatsapp:+{whatsapp_recv_no}"
)

print(f"Message sent! {message.sid}")
