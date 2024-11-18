# WhatsApp Virtual Assistant

This is a PoC of a WhatsApp virtual assistant that creates leads in Salesforce. Built with Langgraph and leveraging Twilio's WhatsApp sandbox.

## Requirements

- [Twilio's WhatsApp Sandbox](https://www.twilio.com/docs/whatsapp/sandbox)
- OpenAI API Key
- Ngrok Account

Then setup your environment variables based on `env.exapmle.sh` in a `env.sh` file and activate them in your terminal: `source env.sh`

## Docker

Build image:

```
make docker-build
```

Run the server

```
make docker-run
```

## Test


You can test that your sandbox is working with the number you used to join:

```
curl http://localhost:5000/test-send-message?to=1234567890
```

### Twilio Sandbox

In your Sandbox settings update the reply endpoint to your grok instance: `https://my-grok-instance.ngrok-free.app/reply`. You should now be able to interact with the LLM through Twilio's WhatsApp.
