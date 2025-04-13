from slack_bolt import App
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])

@app.middleware
def log_request(logger, body, next):
    logger.info(f"REQUEST RECEIVED: {body}")
    next()

@app.event("app_mention")
def handle_mention(event, say, logger):
    logger.info(f"MENTION EVENT RECEIVED: {event}")
    say("aaaaa")

@app.event("message")
def handle_message_event(body, logger, event, client):
    logger.info(f"INCOMING MESSAGE EVENT: {event}")
    if event.get('subtype') is None and event.get('text', '').strip().lower() == 'reee':
        client.chat_postMessage(
            channel=event['channel'],
            text="reeee"
        )

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))