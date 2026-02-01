import json


def judge_lead(conversation, client):
    prompt = f"""
You are a sales qualification expert using the BANT framework.

Return STRICT JSON in this format:
{{
  "qualification": "QUALIFIED | NOT_QUALIFIED",
  "score": 0-100,
  "reasoning": "short explanation"
}}

Conversation:
{conversation}
"""

    response = client.chat.completions.create(
        model="gpt-5.2", messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message.content)
