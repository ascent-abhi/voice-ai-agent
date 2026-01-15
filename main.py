import os
import re
from dotenv import load_dotenv
from openai import OpenAI


from voice_input import listen
from voice_output import speak
from tools import book_meeting, get_time, get_weather


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Memory
memory = [
    {"role": "system", "content": "You are a smart and friendly voice assistant."}
]

print("🤖 Voice AI Agent started. Say 'exit' to stop.")


def extract_datetime(text):
    date = "tomorrow" if "tomorrow" in text.lower() else "today"

    time_match = re.search(r"(\d{1,2})\s*(am|pm)?", text.lower())
    time = time_match.group(0) if time_match else "unspecified time"

    return date, time


# Intent detection
def detect_intent(text):
    text = text.lower()

    if "book" in text:
        return "BOOKING"
    elif "weather" in text:
        return "WEATHER"
    elif "time" in text:
        return "TIME"
    else:
        return "CHAT"


while True:

    user_input = listen()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        speak("Goodbye Abhishek. Have a great day!")
        break

    memory.append({"role": "user", "content": user_input})

    intent = detect_intent(user_input)
    print("Intent:", intent)

    # Tool execution
    if intent == "BOOKING":
        result = book_meeting()
        print("Agent:", result)
        speak(result)
        continue

    if intent == "TIME":
        result = get_time()
        print("Agent:", result)
        speak(result)
        continue

    if intent == "WEATHER":
        result = get_weather()
        print("Agent:", result)
        speak(result)
        continue

    # LLM response
    response = client.chat.completions.create(model="gpt-4o-mini", messages=memory)

    reply = response.choices[0].message.content
    print("Agent:", reply)
    speak(reply)

    memory.append({"role": "assistant", "content": reply})
