from slack_bolt import App
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
app = App(token=slack_bot_token, signing_secret=slack_signing_secret)

TARGET_CHANNEL = "C085QFM80G7" #ewouds-engineering

@app.event("message")
def handle_message_event(body, logger, event, client):
    try:
        logger.info(f"Incoming event: {event}")
        
        if event.get('subtype') is None and event.get('text', '').strip().lower() == 'bbb':
            logger.info("Trigger condition met")
            
            client.conversations_join(channel=TARGET_CHANNEL)
            
            response = client.chat_postMessage(
                channel=TARGET_CHANNEL,
                text="first message sent! :yay:"
            )
            logger.info(f"Message sent: {response}")
            
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))