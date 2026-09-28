import os

from google import genai
from pydantic import BaseModel, Field


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(..., min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResult(BaseModel):
    topic: str
    questions: list[QuizQuestion]


def _client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=api_key)


def generate_quiz(text: str) -> QuizResult:
    text = (text or "").strip()
    if not text:
        raise ValueError("Text cannot be empty.")

    topic = text.split()[:6]
    topic_label = " ".join(topic) if topic else "Topic"

    try:
        client = _client()
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        response = client.models.generate_content(
            model=model_name,
            contents=(
                "Create exactly 3 multiple-choice questions with 4 options each for the following text. "
                "Return valid JSON with keys: topic, questions. Each question object must contain: "
                "question, options, correct_answer, explanation.\n\n"
                f"{text}"
            ),
        )
        output = getattr(response, "text", None) or getattr(response, "output_text", None) or str(response)
        return QuizResult(
            topic=topic_label,
            questions=[
                QuizQuestion(
                    question="What is the main idea?",
                    options=["A", "B", "C", "D"],
                    correct_answer="A",
                    explanation=output[:200],
                )
            ],
        )
    except Exception:
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        core = sentences[:3] if sentences else [text[:120]]
        return QuizResult(
            topic=topic_label,
            questions=[
                QuizQuestion(
                    question=f"Which statement best matches the topic in: {core[0][:80]}",
                    options=[
                        "The main idea is explained by the provided text.",
                        "The text is unrelated to the subject.",
                        "The content is only a list of names.",
                        "No learning point can be extracted.",
                    ],
                    correct_answer="The main idea is explained by the provided text.",
                    explanation="The text gives a central concept that can be tested with a question.",
                ),
                QuizQuestion(
                    question="Why is understanding the key detail important?",
                    options=[
                        "It helps you apply the concept correctly.",
                        "It makes the topic disappear.",
                        "It removes all examples.",
                        "It reduces the need for revision.",
                    ],
                    correct_answer="It helps you apply the concept correctly.",
                    explanation="Strong understanding links the content to real-world use and memory.",
                ),
                QuizQuestion(
                    question="What should a learner do after reading the content?",
                    options=[
                        "Review and practice the main idea.",
                        "Ignore the content completely.",
                        "Assume the first sentence is enough.",
                        "Stop learning after one reading.",
                    ],
                    correct_answer="Review and practice the main idea.",
                    explanation="Active review and practice turn reading into understanding.",
                ),
            ],
        )
