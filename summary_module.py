import os

from google import genai


def _client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=api_key)


def summarize_text(text: str) -> str:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    try:
        client = _client()
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        response = client.models.generate_content(
            model=model_name,
            contents=(
                "Summarize the following text clearly and simply for learning revision:\n\n"
                f"{text}"
            ),
        )
        text_out = getattr(response, "text", None) or getattr(response, "output_text", None)
        if text_out:
            return text_out.strip()
        return str(response).strip()
    except Exception:
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if not sentences:
            return "No summary available."
        summary = " ".join(sentences[:3])
        return summary + ("..." if len(sentences) > 3 else "")
