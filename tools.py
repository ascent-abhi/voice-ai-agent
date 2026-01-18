import re
from datetime import datetime


def extract_datetime(text):
    text = text.lower()

    date = "tomorrow" if "tomorrow" in text else "today"

    time_match = re.search(r"(\d{1,2})\s*(am|pm)?", text)
    time = time_match.group(0) if time_match else "unspecified time"

    return date, time


def book_meeting(text):
    date, time = extract_datetime(text)
    return f"✅ Your meeting is booked for {date} at {time}."


def get_time():
    return f"The current time is {datetime.now().strftime('%H:%M')}"


def get_weather():
    return "It's sunny today."


def conversation_to_text(memory):
    text = ""
    for msg in memory:
        text += f"{msg['role']}: {msg['content']}\n"
    return text
