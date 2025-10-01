"""LLM utilities using LiteLLM - reused from bcp version."""

import os
import asyncio
from typing import Optional
import litellm
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """LLM client using LiteLLM library for multiple provider support."""

    def __init__(self):
        """Initialize LiteLLM client."""
        self.provider = os.getenv("LLM_PROVIDER", "ollama")

        if self.provider == "ollama":
            self.model = f"ollama/{os.getenv('OLLAMA_MODEL', 'mistral:latest')}"
            ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            if ollama_base_url:
                litellm.api_base = ollama_base_url

        elif self.provider == "gemini":
            self.model = "gemini/gemini-pro"

        else:
            self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

        self.temperature = 0.1

    def invoke(self, message: str, system_prompt: Optional[str] = None) -> "LLMResponse":
        """Sync invoke method."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})

        try:
            response = litellm.completion(
                model=self.model,
                messages=messages,
                temperature=self.temperature
            )
            content = response.choices[0].message.content
            return LLMResponse(content=content)

        except Exception as e:
            fallback_content = f"LLM error: {str(e)}"
            return LLMResponse(content=fallback_content)


class LLMResponse:
    """LLM response wrapper."""

    def __init__(self, content: str):
        self.content = content

    def __str__(self):
        return self.content


def get_llm() -> LLMClient:
    """Get configured LLM client."""
    return LLMClient()
