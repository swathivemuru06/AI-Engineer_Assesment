# tests/test_llm.py

import pytest
from unittest.mock import MagicMock
from llm import answer_with_context

def test_answer_with_context(monkeypatch):
    # Mock the LLMChain.run method so no real OpenAI API call happens
    def fake_run(self, inputs):
        return "Mocked answer"

    monkeypatch.setattr(
        "llm_client.LLMChain.run",
        fake_run
    )

    output = answer_with_context("test context", "test question")

    assert output == "Mocked answer"
