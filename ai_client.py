import os

import httpx


BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = os.getenv("LLM_MODEL", "gemini-3.6-flash")
EMBED_MODEL = "gemini-embedding-001"


def request_google(path, body):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Set GEMINI_API_KEY in this terminal before running."
        )

    response = httpx.post(
        f"{BASE_URL}/{path}",
        headers={"x-goog-api-key": api_key},
        json=body,
        timeout=120.0,
    )

    if not response.is_success:
        raise RuntimeError(
            f"Gemini API returned HTTP {response.status_code}: "
            f"{response.text}"
        )

    return response.json()


def generate(prompt, temperature=0.2, json_mode=False):
    generation_config = {
        "temperature": temperature,
        "maxOutputTokens": 2048,
    }

    # Disable thinking for this particular model so the small
    # experiments focus on visible responses and their token usage.
    if MODEL == "gemini-2.5-flash":
        generation_config["thinkingConfig"] = {
            "thinkingBudget": 0
        }

    if json_mode:
        generation_config["responseMimeType"] = "application/json"

    body = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": generation_config,
    }

    result = request_google(
        f"models/{MODEL}:generateContent",
        body,
    )

    candidates = result.get("candidates", [])

    if not candidates:
        raise RuntimeError(
            "The API returned no answer candidate. "
            f"Feedback: {result.get('promptFeedback', {})}"
        )

    candidate = candidates[0]

    if candidate.get("finishReason") != "STOP":
        raise RuntimeError(
            "The answer did not finish normally. "
            f"Reason: {candidate.get('finishReason')}"
        )

    parts = candidate.get("content", {}).get("parts", [])

    answer = "".join(
        part.get("text", "")
        for part in parts
        if not part.get("thought", False)
    )

    if not answer.strip():
        raise RuntimeError("The API returned no usable answer text.")

    usage = result.get("usageMetadata", {})

    # Keep the field names used by your existing lab scripts.
    return {
        "response": answer,
        "prompt_eval_count": usage.get("promptTokenCount"),
        "eval_count": usage.get("candidatesTokenCount"),
        "model": MODEL,
    }


def embed(texts):
    vectors = []

    for text in texts:
        result = request_google(
            f"models/{EMBED_MODEL}:embedContent",
            {
                "model": f"models/{EMBED_MODEL}",
                "content": {
                    "parts": [{"text": text}]
                },
                "taskType": "SEMANTIC_SIMILARITY",
                "outputDimensionality": 768,
            },
        )

        vectors.append(result["embedding"]["values"])

    return vectors