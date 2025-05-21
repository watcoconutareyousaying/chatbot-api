# 🦷 Dental Anatomy Bot API

An AI-powered API built with FastAPI and LangChain, designed for dental anatomy applications. It supports local LLMs via Ollama and integrates with OpenAI and DeepSeek APIs for advanced question-answering, educational tools, and clinical support. Ideal for dental students, educators, and healthcare developers.

### ✨ Features
- FastAPI-based RESTful API
- LangChain-powered reasoning
- Local LLM support via Ollama
- OpenAI and DeepSeek integration
- RAG (Retrieval-Augmented Generation)
- Focused on dental anatomy knowledge

---

## 📦 Alembic Migration Guide

This project uses **Alembic** for managing database schema migrations.

### ✅ Initial Setup

1. Ensure Alembic is installed:

   ```bash
   pip install alembic

2. Make sure all your SQLAlchemy models are imported in alembic/env.py so Alembic can detect them.

3. Create a new migration (auto-detect model changes):
    ```bash
    alembic revision --autogenerate -m "your descriptive message"

4. Apply latest migrations to the database:
    ```bash
    alembic upgrade head

5. Roll back the last migration:
    ```bash
    alembic downgrade -1

6. View migration history:
    ```bash
    alembic history