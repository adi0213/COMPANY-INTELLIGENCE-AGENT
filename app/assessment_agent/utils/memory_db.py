import time

# Store a history of generated questions to prevent duplicates
# Structure: list of dicts: {"text": "question text", "timestamp": float, "type": "coding|aptitude"}
generated_question_history = []

def add_to_history(question_text: str, q_type: str):
    generated_question_history.append({
        "text": question_text,
        "timestamp": time.time(),
        "type": q_type
    })

def get_recent_history(q_type: str, limit: int = 50) -> list:
    filtered = [q["text"] for q in generated_question_history if q["type"] == q_type]
    # Return the most recent 'limit' questions
    return filtered[-limit:]
