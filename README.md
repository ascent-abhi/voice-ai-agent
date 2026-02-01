# 📞 AI Voice Sales Agent (Applied AI)

## Overview

The **AI Voice Sales Agent** is a Python-based applied AI system that simulates a real-world outbound sales call.
It conducts a structured sales conversation using the **BANT qualification framework** and delegates final lead qualification to an LLM-based judge.

This project focuses on **system design, agent orchestration, and real-world AI reliability**, rather than building a simple chatbot.

---

## Key Objectives

* Simulate a realistic AI-driven sales calling agent
* Keep conversation flow **deterministic and testable**
* Use LLMs only where **judgment is required**
* Generate **structured outputs**, not free text
* Design for **failure handling** and real-world constraints

---

## High-Level Flow

1. Agent initiates a mock sales call
2. Conducts a step-by-step BANT qualification conversation
3. Collects lead data during the call
4. Passes full conversation transcript to an LLM judge
5. Receives structured qualification decision
6. Saves lead data to a mock database
7. Responds appropriately to the lead

---

## Architecture Overview

```
ai_sales_agent/
│
├── main.py                # Orchestration / runtime loop
│
├── agent/
│   ├── sales_agent.py     # Conversation logic + state machine
│   └── steps.py           # Agent state definitions
│
├── models/
│   └── lead.py            # Lead data schema
│
├── llm/
│   └── judge.py           # LLM-based lead qualification
│
├── io/
│   ├── voice_input.py     # Speech-to-text abstraction
│   └── voice_output.py    # Text-to-speech abstraction
│
├── storage/
│   └── mock_db.py         # Mock persistence layer
│
├── utils/
│   └── conversation.py    # Conversation formatting utilities
│
└── .env
```

---

## Design Principles

### 1. Deterministic Agent Flow

* The agent follows a **fixed state machine**
* LLMs do **not** control conversation flow
* Each step explicitly transitions to the next

### 2. LLMs Used for Judgment Only

* LLM evaluates the conversation at the end
* No prompt chaining or agent hallucinations
* Structured JSON output enforced

### 3. Real-World Reliability

* LLM failures (quota, timeout) are handled gracefully
* System falls back to a `PENDING_REVIEW` state
* Leads are always persisted

### 4. Separation of Concerns

* Agent logic, LLM calls, IO, and storage are isolated
* Easy to test, refactor, and extend

---

## Sales Qualification Framework (BANT)

The agent qualifies leads based on:

* **Budget** – Willingness or ability to invest
* **Authority** – Decision-making capability
* **Need** – Identified pain points
* **Timeline** – Urgency and implementation window

A lead is considered **qualified** if it satisfies at least **3 out of 4 BANT criteria**.

---

## Lead Data Model

```python
Lead:
- pain_points: list
- current_tool: str
- authority: str
- budget: str
- timeline: str
- company_size: str
- qualification: str
- score: int
- reasoning: str
```

This ensures all AI outputs are **structured and machine-readable**.

---

## LLM Judge Output Format

The LLM judge returns **strict JSON**:

```json
{
  "qualification": "QUALIFIED | NOT_QUALIFIED | PENDING_REVIEW",
  "score": 0-100,
  "reasoning": "Short explanation"
}
```

---

## Error Handling & Fallback Strategy

If the LLM is unavailable due to quota or network issues:

* The system does **not crash**
* Qualification is set to `PENDING_REVIEW`
* Lead data is still saved
* User receives a polite fallback response

This mirrors real-world production behavior.

---

## Running the Project

### Prerequisites

* Python 3.9+
* OpenAI API key

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
USE_LLM=true
```

(Optional for development)

```
USE_LLM=false
```

### Run

```bash
python main.py
```

---

## Current Status

✅ Agent state machine implemented
✅ Structured lead data model
✅ LLM-based judge with fallback
✅ Mock persistence layer
✅ Voice IO abstraction
✅ Interview-ready architecture

---

## Planned Enhancements (Future Scope)

* Confidence scoring before LLM judgment
* Objection detection and handling
* Partial qualification states
* Conversation memory summarization
* REST API exposure (FastAPI)
* Database integration (PostgreSQL)

---

## Why This Project Matters

This project demonstrates:

* Applied AI system design
* Real-world LLM usage patterns
* Backend engineering discipline
* Failure-aware architecture
* Production-style thinking

It is intentionally **not** a chatbot demo.

---

## Author

**Abhishek Padaya**
Backend Engineer | Applied AI Systems
LinkedIn: [https://www.linkedin.com/in/abhishek-padaya/](https://www.linkedin.com/in/abhishek-padaya/)
GitHub: [https://github.com/ascent-abhi](https://github.com/ascent-abhi)

---

## Mentor Note (Not in README)

This README is:

* ATS-friendly
* Recruiter-readable
* Interview-defensible
* Honest (no hype)

If you want next, we can:

* Add **architecture diagram**
* Add **sample conversation transcript**
* Add **demo mode instructions**
* Rewrite this README for **GitHub stars vs recruiters**

Just tell me the next move.
