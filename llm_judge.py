def judge_lead(conversation, client):

    prompt = f"""
You are a sales qualification expert.

Based on the conversation below,
decide if the lead is QUALIFIED.

Rules:
- Interested in product?
- Decision maker or influencer?
- Company size > 10 is positive
- Open to demo is positive

Conversation:
{conversation}

Respond ONLY with:
QUALIFIED
or
NOT_QUALIFIED
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
