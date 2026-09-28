import os

from google import genai


def _client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=api_key)


def get_learning_recommendations(topic: str, level: str = "beginner") -> list[dict]:
    topic = (topic or "").strip()
    level = (level or "beginner").strip().lower()
    if not topic:
        raise ValueError("Topic cannot be empty.")

    level_map = {
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
    }
    label = level_map.get(level, "Beginner")

    try:
        client = _client()
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        response = client.models.generate_content(
            model=model_name,
            contents=(
                f"Create a useful learning roadmap for '{topic}' at the {label} level. "
                "Return it as a short JSON array with 3 items, each containing: "
                "title, description, and resources."
            ),
        )
        text = getattr(response, "text", None) or getattr(response, "output_text", None) or str(response)
        return [{
            "title": "AI-generated roadmap",
            "description": text.strip(),
            "resources": ["Review notes", "Practice questions", "Mini project"],
        }]
    except Exception:
        return [
            {
                "title": f"Foundation in {topic}",
                "description": f"Learn the basic definitions, terms, and key examples for {topic} before moving deeper.",
                "resources": ["Intro article", "Short video lesson", "Basic exercises"],
            },
            {
                "title": f"Application of {topic}",
                "description": f"Practice solving real tasks and examples so the concept becomes usable in context.",
                "resources": ["Sample problems", "Workbook practice", "Hands-on examples"],
            },
            {
                "title": f"Advanced work in {topic}",
                "description": f"Once the basics are steady, explore deeper questions, edge cases, and more complex scenarios.",
                "resources": ["Case studies", "Advanced reading", "Capstone challenge"],
            },
        ]
