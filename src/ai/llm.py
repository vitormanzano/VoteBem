import time

from groq import Groq, APIConnectionError, APIStatusError

import config

_client: Groq | None = None


def get_client() -> Groq:
    global _client
    if _client is None:
        if not config.GROQ_API_KEY:
            raise RuntimeError(
                "GROQ_API_KEY não configurada — preencha src/ai/.env"
            )
        _client = Groq(api_key=config.GROQ_API_KEY)
    return _client


def chat_completion(
    messages: list[dict],
    tools: list[dict] | None = None,
    temperature: float = 0.1,
    max_tokens: int = 1024,
    retries: int = 3,
    model: str | None = None,
):
    """Chamada ao Groq com retry exponencial em erros transitórios.

    `model` sobrescreve o default de config.GROQ_MODEL — útil para
    rodar batches em modelos mais leves sem mexer no .env do servidor.
    """
    client = get_client()
    last_error: Exception | None = None

    for attempt in range(retries):
        try:
            kwargs = {
                "model": model or config.GROQ_MODEL,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"
            return client.chat.completions.create(**kwargs)
        except (APIConnectionError, APIStatusError) as e:
            last_error = e
            if attempt == retries - 1:
                break
            time.sleep(1.5 * (attempt + 1))

    raise last_error  # type: ignore[misc]
