# notifier-service
A simple http service to send notification througt Telegram bot

## Hot to use it

To use this service you need `Python >= 3.7`
Install dependencies:

```bash
pipenv install
# OR
pip install -r requirements.txt
```

After that you can create a bot asking to BotFather, follow the [Telegram guide](https://core.telegram.org/bots#6-botfather). 

Then you can use the token to register and make your own notification service:

```bash
# Start the service
python notify_service.py admin password secret

# Register the Telegram Bot
curl -X POST -u admin:password localhost:5555/botRegister -d bot_token="telegram token"
# SUCCESS OUTPUT:
# {"message":"BOT STARTED!","status":"OK"}
```

At this point open a chat with your bot and get your ids to procede:

```bash
# Signup with your credentials
curl -X POST -u admin:password localhost:5555/signup -d user_id="your_user_id" -d chat_id="your_chat_id"
# SUCCESS OUTPUT:
# {"service_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJib3RfdG9rZW4iOiJmb29iYXIiLCJ1c2VyX2lkIjoidGVzdCIsImNoYXRfaWQiOiJ0ZXN0In0.l4thYfm2xUOaCOBWBMKzoYTlUsN1i4jDaAD8_gxdElA"}
```

After that you can use the service to send you message throught your service:

```bash
curl -X POST localhost:5555/notify -d message="Hello World" -d service_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJib3RfdG9rZW4iOiJmb29iYXIiLCJ1c2VyX2lkIjoidGVzdCIsImNoYXRfaWQiOiJ0ZXN0In0.l4thYfm2xUOaCOBWBMKzoYTlUsN1i4jDaAD8_gxdElA"
# SUCCESS OUTPUT:
# {"message_sent":"Hello World","status":"OK"}
```