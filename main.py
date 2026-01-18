import os

from dotenv import load_dotenv
from openai import OpenAI


from voice_input import listen
from voice_output import speak
from sales_logic import score_lead
from tools import conversation_to_text
from llm_judge import judge_lead

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt (agent brain)
memory = [
    {
        "role": "system",
        "content": """
You are an AI sales calling agent.

Your goal:
Qualify leads for a product demo.

Conversation flow:
1. Introduce yourself
2. Ask if user is decision maker
3. Ask what software they currently use
4. Ask company size
5. Decide QUALIFIED or NOT QUALIFIED
6. If qualified → offer demo booking

Rules:
- Ask only ONE question at a time
- Be polite and friendly
- Keep responses short
""",
    }
]

lead_data = {"decision_maker": "", "current_tool": "", "company_size": ""}

current_step = "INTRO"

print("📞 Sales AI Agent started...")


def get_ai_reply():
    response = client.chat.completions.create(model="gpt-4o-mini", messages=memory)
    return response.choices[0].message.content


while True:

    if current_step == "INTRO":
        intro = (
            "Hi, this is Alex from XYZ Solutions. "
            "You recently downloaded our guide on improving sales productivity. "
            "I’m calling to understand your current process and see if we can help."
        )

        speak(intro)
        memory.append({"role": "assistant", "content": intro})
        current_step = "DECISION"
        continue

    user_input = listen()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        speak("Thank you. Have a great day!")
        break

    memory.append({"role": "user", "content": user_input})

    # Step handling
    if current_step == "DECISION":
        ai = "Are you the decision maker for software purchases?"
        speak(ai)
        memory.append({"role": "assistant", "content": ai})
        current_step = "WAIT-DECISION"
        continue

    if current_step == "WAIT-DECISION":
        lead_data["decision_maker"] = user_input
        ai = "What software do you currently use?"
        speak(ai)
        memory.append({"role": "assistant", "content": ai})
        current_step = "WAIT-TOOL"
        continue

    if current_step == "WAIT-TOOL":
        lead_data["current_tool"] = user_input
        ai = "What is your company size?"
        speak(ai)
        memory.append({"role": "assistant", "content": ai})
        current_step = "WAIT-SIZE"
        continue

    if current_step == "WAIT-SIZE":
        lead_data["company_size"] = user_input

    conversation = conversation_to_text(memory)
    decision = judge_lead(conversation, client)

    print("LLM decision:", decision)

    if decision == "QUALIFIED":
        ai = "Great! You seem like a good fit. Would you like to book a free demo?"
    else:
        ai = "Thanks for your time. At the moment we may not be the right fit."

    speak(ai)
    memory.append({"role": "assistant", "content": ai})
    break
