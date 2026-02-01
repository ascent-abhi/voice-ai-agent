def conversation_to_text(memory):
    return "\n".join(f"{m['role']}: {m['content']}" for m in memory)
