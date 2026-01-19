def judge_lead(conversation, client):

    prompt = f"""
You are a sales qualification expert using the BANT framework (Budget, Authority, Need, Timeline).

Based on the conversation below, decide if the lead is QUALIFIED using these real-world criteria:

BANT QUALIFICATION CRITERIA:
1. BUDGET:
   - Has budget allocated or approved for software purchases
   - Mentions willingness to invest
   - Discusses pricing or payment terms
   - Has budget authority or approval process

2. AUTHORITY:
   - Decision maker or key influencer in purchase decisions
   - VP, Director, Manager, Owner, or C-level titles
   - Has authority to sign off on purchases
   - Involved in vendor evaluation

3. NEED:
   - Identified pain points or challenges
   - Current solution frustrations or limitations
   - Business problems that need solving
   - Clear use case or business need

4. TIMELINE:
   - Specific timeline mentioned (month, quarter, year)
   - Urgency indicators (soon, ASAP, immediately)
   - Project deadlines or implementation dates
   - Active evaluation process

ADDITIONAL QUALIFYING SIGNALS:
- Company size > 10 employees (better fit)
- Open to demo or next steps
- Asks specific questions about features
- Compares with competitors
- Shows genuine interest

DISQUALIFYING FACTORS:
- No budget or budget constraints
- Not a decision maker and no access to one
- No clear pain point or need
- No timeline or "maybe next year"
- Already committed to another vendor
- Too small company size for product fit

Conversation:
{conversation}

Evaluate based on BANT criteria. A lead needs to meet at least 3 out of 4 BANT criteria to be QUALIFIED.

Respond ONLY with:
QUALIFIED
or
NOT_QUALIFIED
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
