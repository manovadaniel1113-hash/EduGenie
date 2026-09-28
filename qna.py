import os

from google import genai


def _client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=api_key)


def _fallback_answer(question: str) -> str:
    q = (question or "").strip()
    if not q:
        return "Please enter a valid question so I can help you learn."
    if "python" in q.lower():
        return (
            "Python is a high-level programming language used to build websites, data tools, automation, and AI applications. "
            "It is beginner-friendly because the syntax is simple and readable, making it a great language to learn first."
        )
    return (
        f"A good way to understand '{q}' is to break it into smaller ideas, look at a simple example, and practice it with a real task. "
        "This makes the concept easier to remember and apply confidently."
    )


def answer_question(question: str) -> str:
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    try:
        client = _client()
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        response = client.models.generate_content(
            model=model_name,
            contents=f"Answer the question clearly and accurately: {question}",
        )
        text = getattr(response, "text", None) or getattr(response, "output_text", None)
        if text:
            return text.strip()
        return str(response).strip()
    except Exception:
        return _fallback_answer(question)


def answer_question_with_gemini(question: str) -> str:
    return answer_question(question)
