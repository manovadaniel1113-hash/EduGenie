
# EduGenie

Google Gemini Powered Learning Assistant.

EduGenie is a FastAPI + HTML/CSS/JavaScript educational assistant.

It provides:

- Question answering
- Concept explanation
- Quiz generation
- Text summarization
- Personalized learning paths


# Project Structure

```text
EduGenie/
│
├── main.py
├── config.py
├── models.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
│
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── app.js
│
└── tests/
    └── test_app.py
