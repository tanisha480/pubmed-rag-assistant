import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("GROQ_API_KEY", "test-key")

import query


def test_answer_question_returns_fallback_when_no_context(monkeypatch):
    monkeypatch.setattr(query, "embed", lambda text: [0.0] * 10)
    monkeypatch.setattr(query.collection, "query", lambda **kwargs: {"metadatas": [[]]})

    answer, chunks = query.answer_question("What is aspirin?")

    assert "don't have any relevant information" in answer
    assert chunks == []


def test_answer_question_returns_llm_answer_with_context(monkeypatch):
    monkeypatch.setattr(query, "embed", lambda text: [0.0] * 10)
    fake_chunks = [{"context": "Aspirin reduces inflammation."}]
    monkeypatch.setattr(query.collection, "query", lambda **kwargs: {"metadatas": [fake_chunks]})

    fake_response = MagicMock()
    fake_response.choices = [MagicMock(message=MagicMock(content="Aspirin is an anti-inflammatory drug."))]
    monkeypatch.setattr(query.groq_client.chat.completions, "create", lambda **kwargs: fake_response)

    answer, chunks = query.answer_question("What does aspirin do?")

    assert answer == "Aspirin is an anti-inflammatory drug."
    assert chunks == ["Aspirin reduces inflammation."]
