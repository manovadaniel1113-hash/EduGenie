import os

from google import genai


def _client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=api_key)


def explain_topic(topic: str) -> str:
    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty.")

    try:
        client = _client()
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        response = client.models.generate_content(
            model=model_name,
            contents=(
                f"Explain the concept of '{topic}' in a simple, child-friendly way, "
                "using clear examples and a short structure."
            ),
        )
        text = getattr(response, "text", None) or getattr(response, "output_text", None)
        if text:
            return text.strip()
        return str(response).strip()
    except Exception:
        return (
            f"Here is a simple explanation of '{topic}':\n\n"
            f"{topic} is a concept that can be understood by breaking it into smaller parts. "
            "Start with the basic idea, look at a real-world example, then connect it to a simple task or question. "
            "This makes the topic easier to remember and apply in everyday learning."
        )
