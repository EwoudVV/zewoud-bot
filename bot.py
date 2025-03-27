from slack_bolt import App
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])

@app.event("message")
def handle_message_event(body, logger, event, client):
    try:
        logger.info(f"Incoming event: {event}")
        
        if event.get('subtype') is None and event.get('text', '').strip().lower() == 'work pls':
            logger.info("Trigger condition met")
            
            response = client.chat_postMessage(
                channel=event['channel'],
                text="first message sent! :yay:"
            )
            logger.info(f"Message sent: {response}")
            
    except Exception as e:
        logger.error(f"Error: {e}")

@app.event("app_mention")
def handle_mention(event, say):
    say("this better work")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))