import requests
from ics import Calendar
from datetime import datetime, timedelta
import pytz
import os

def get_due_tomorrow(ellie_user_id):
    ical_url = os.environ["CALENDAR_ICAL"]
    response = requests.get(ical_url)

    if response.status_code != 200:
        return f"<@{ellie_user_id}> could not fetch Schoology calendar"

    try:
        calendar = Calendar(response.text)
    except Exception:
        return f"<@{ellie_user_id}> calendar could not be parsed"

    tz = pytz.timezone("America/New_York")
    today = datetime.now(tz)
    tomorrow = today + timedelta(days=1)

    due = []
    for event in calendar.events:
        event_time = event.begin.astimezone(tz)
        if event_time.date() == tomorrow.date():
            due.append(event.name.strip())

    if due:
        return f"<@{ellie_user_id}> due tomorrow: " + ", ".join(due)
    else:
        return f"<@{ellie_user_id}> nothing due tomorrow"