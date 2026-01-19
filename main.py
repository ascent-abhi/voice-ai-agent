import os

from dotenv import load_dotenv
from openai import OpenAI


from voice_input import listen
from voice_output import speak

from tools import conversation_to_text
from llm_judge import judge_lead

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt (agent brain)
memory = [
    {
        "role": "system",
        "content": """
You are an AI sales calling agent specializing in BANT qualification (Budget, Authority, Need, Timeline).

Your goal:
Qualify leads for a product demo using real-world sales metrics.

Conversation flow:
1. Introduce yourself
2. Identify pain points and needs (Need)
3. Confirm decision-making authority (Authority)
4. Understand current solutions and challenges
5. Explore budget and investment readiness (Budget)
6. Determine implementation timeline (Timeline)
7. Collect company size and industry context
8. Decide QUALIFIED or NOT QUALIFIED
9. If qualified → offer demo booking

Rules:
- Ask only ONE question at a time
- Be polite, friendly, and consultative
- Keep responses short (1-2 sentences max)
- Listen for buying signals and objections
- Adapt questions based on responses
""",
    }
]

# Comprehensive lead data structure for real-world qualification
lead_data = {
    "decision_maker": "",
    "authority_level": "",
    "current_tool": "",
    "pain_points": [],
    "company_size": "",
    "industry": "",
    "budget": "",
    "budget_timeline": "",
    "timeline": "",
    "urgency": "",
    "use_case": "",
    "objections": [],
    "buying_signals": [],
}

current_step = "INTRO"

print("📞 Sales AI Agent started...")
print("🎯 Using BANT qualification framework (Budget, Authority, Need, Timeline)")


def get_ai_reply():
    response = client.chat.completions.create(model="gpt-4o-mini", messages=memory)
    return response.choices[0].message.content


while True:

    if current_step == "INTRO":
        intro = (
            "Hi, this is Alex from XYZ Solutions. "
            "You recently downloaded our guide on improving sales productivity. "
            "I'm calling to understand your current challenges and see if we can help."
        )

        speak(intro)
        memory.append({"role": "assistant", "content": intro})
        current_step = "PAIN_POINTS"
        continue

    user_input = listen()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        speak("Thank you. Have a great day!")
        break

    memory.append({"role": "user", "content": user_input})

    # BANT Qualification Flow with Real-World Metrics

    if current_step == "PAIN_POINTS":
        # Identify Need (N in BANT)
        ai = "What's the biggest challenge you're facing with your current sales process or tools?"
        speak(ai)
        memory.append({"role": "assistant", "content": ai})
        current_step = "WAIT-PAIN"
        continue

    if current_step == "WAIT-PAIN":
        lead_data["pain_points"].append(user_input)
        # Always ask about current tools to understand their situation better
        ai = "What software or tools are you currently using for sales?"
        speak(ai)
        memory.append({"role": "assistant", "content": ai})
        current_step = "WAIT-TOOL"
        continue

    if current_step == "WAIT-TOOL":
        lead_data["current_tool"] = user_input
        # Check Authority (A in BANT)
        ai = "Are you involved in making decisions about software purchases for your team?"
        speak(ai)
        memory.append({"role": "assistant", "content": ai})
        current_step = "WAIT-AUTHORITY"
        continue

    if current_step == "WAIT-AUTHORITY":
        lead_data["decision_maker"] = user_input
        lead_data["authority_level"] = user_input
        # Budget (B in BANT)
        ai = "Do you have a budget allocated for improving your sales tools this quarter or year?"
        speak(ai)
        memory.append({"role": "assistant", "content": ai})
        current_step = "WAIT-BUDGET"
        continue

    if current_step == "WAIT-BUDGET":
        lead_data["budget"] = user_input
        # Timeline (T in BANT)
        ai = "What's your timeline for implementing a solution? Is this something you're looking to address soon?"
        speak(ai)
        memory.append({"role": "assistant", "content": ai})
        current_step = "WAIT-TIMELINE"
        continue

    if current_step == "WAIT-TIMELINE":
        lead_data["timeline"] = user_input
        # Company context for better qualification
        ai = "Just to better understand your needs, how many employees are in your company?"
        speak(ai)
        memory.append({"role": "assistant", "content": ai})
        current_step = "WAIT-SIZE"
        continue

    if current_step == "WAIT-SIZE":
        lead_data["company_size"] = user_input

        # Use LLM judge for final decision (single source of truth)
        conversation = conversation_to_text(memory)
        decision = judge_lead(conversation, client)

        print(f"\n🤖 LLM Judge Decision: {decision}\n")

        if decision == "QUALIFIED":
            ai = (
                "Great! Based on what you've shared, you seem like an excellent fit. "
                "Would you like to book a free demo where I can show you exactly how we can help?"
            )
        else:
            ai = (
                "I appreciate you taking the time to share that information. "
                "Based on what you've told me, we may not be the best fit right now, "
                "but I'd be happy to send you some resources that might be helpful."
            )

        speak(ai)
        memory.append({"role": "assistant", "content": ai})
        break
