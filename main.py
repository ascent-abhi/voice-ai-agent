import os
from dotenv import load_dotenv
from openai import OpenAI

from agent.sales_agent import SalesAgent
from agent.steps import AgentStep
from llm.judge import judge_lead
from storage.mock_db import MockLeadDB
from utils.conversation import conversation_to_text
from voice.voice_input import listen
from voice.voice_output import speak

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

agent = SalesAgent()
db = MockLeadDB()

print("📞 AI Sales Agent started")

while agent.step != AgentStep.JUDGEMENT:

    prompt = agent.get_next_prompt()
    if prompt:
        speak(prompt)
        agent.memory.append({"role": "assistant", "content": prompt})

    user_input = listen()
    if not user_input:
        continue

    if user_input.lower() == "exit":
        speak("Thank you for your time. Have a great day!")
        break

    agent.memory.append({"role": "user", "content": user_input})
    agent.handle_user_response(user_input)

# Final LLM-based decision
conversation = conversation_to_text(agent.memory)
decision = judge_lead(conversation, client)

agent.lead.qualification = decision["qualification"]
agent.lead.score = decision["score"]
agent.lead.reasoning = decision["reasoning"]

db.save(agent.lead)

if agent.lead.qualification == "QUALIFIED":
    speak("Great news! You look like a strong fit. Would you like to book a demo?")
else:
    speak(
        "Thanks for sharing your details. I’ll share some helpful resources with you."
    )
