"""Streaming answer generator for the legal RAG pipeline."""

import logging
from collections.abc import Generator

import groq

from config import GROQ_API_KEY, GROQ_MODEL
from rag.prompts import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)

_client = groq.Groq(api_key=GROQ_API_KEY)


def generate(question: str, chunks: list[dict]) -> Generator[str, None, None]:
    """Stream answer tokens from Groq given a question and retrieved chunks."""
    user_prompt = build_user_prompt(chunks, question)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    try:
        stream = _client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content is not None:
                yield content
    except groq.RateLimitError:
        logger.warning("Groq rate limit hit")
        yield "Demo is currently busy — please try again in a moment."
    except groq.APIConnectionError:
        logger.error("Groq connection error")
        yield "Unable to reach the AI service. Please try again."
    except Exception as e:
        logger.error("Groq request failed: %s", e)
        yield "An unexpected error occurred. Please try again."
