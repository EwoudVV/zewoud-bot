from slack_bolt import App
from apscheduler.schedulers.background import BackgroundScheduler
import os
import logging
from dotenv import load_dotenv
from schoology_due_check import get_due_tomorrow

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

ELLIE_SLACK_USER_ID = "idk"
ELLIES_ENGINEERING_CHANNEL_ID = "idk"

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
    if event.get('subtype') is None:
        text = event.get('text', '').strip().lower()

        if text == 'reee':
            client.chat_postMessage(channel=event['channel'], text="reeee")

        elif text == 'due tomorrow':
            msg = get_due_tomorrow(ELLIE_SLACK_USER_ID)
            client.chat_postMessage(channel=event["channel"], text=msg)

def send_daily_schoology_check():
    msg = get_due_tomorrow(ELLIE_SLACK_USER_ID)
    if msg:
        app.client.chat_postMessage(channel=ELLIES_ENGINEERING_CHANNEL_ID, text=msg)

scheduler = BackgroundScheduler(timezone="America/New_York")
scheduler.add_job(send_daily_schoology_check, 'cron', hour=14, minute=0)
scheduler.start()

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
