# WhatsApp Virtual Assistant

This is a PoC of a WhatsApp virtual assistant that creates leads in Salesforce. Built with Langgraph and leveraging Twilio's WhatsApp sandbox.

## Requirements

- [Twilio's WhatsApp Sandbox](https://www.twilio.com/docs/whatsapp/sandbox)
- OpenAI API Key
- Ngrok Account
- [Salesforce Developer Edition](https://developer.salesforce.com/signup)

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

### Salesforce JWT + Connected App

You need to setup JWT Server-to-Server flow with a Connected App. [Here is a useful guide](https://medium.com/@sfdcpulse/salesforce-oauth-jwt-bearer-flow-for-server-to-salesforce-integration-27c7ffbbe946)

### Twilio Sandbox

In your Sandbox settings update the reply endpoint to your grok instance: `https://my-grok-instance.ngrok-free.app/reply`. You should now be able to interact with the virtual assistant through Twilio's WhatsApp.
