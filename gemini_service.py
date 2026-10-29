from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    logger,
)

STYLE_PROMPTS = {
    "professional": (
        "Rewrite the text in professional business "
        "English, using clear and natural wording."
    ),
    "polite": ("Rewrite the text in a polite, respectful " "and friendly tone."),
    "simple": ("Rewrite the text in simple, clear and " "easy-to-understand English."),
    "formal": (
        "Rewrite the text in formal English " "suitable for official communication."
    ),
}

_client = None


def get_client():
    global _client

    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is missing. " "Please configure it in your .env file."
        )

    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)

    return _client


def rephrase_text(text, style):
    text = text.strip()

    if not text:
        raise ValueError("Please enter text to rephrase.")

    if style not in STYLE_PROMPTS:
        raise ValueError(f"Unsupported writing style: {style}")

    logger.info(
        "Rephrase request started | " "style=%s | chars=%d",
        style,
        len(text),
    )

    prompt = (
        f"{STYLE_PROMPTS[style]}\n\n"
        "Rules:\n"
        "1. Preserve the original meaning.\n"
        "2. Correct grammar and spelling.\n"
        "3. Do not invent new information.\n"
        "4. Return only the rewritten text.\n"
        "5. Do not include explanations.\n\n"
        f"Original text:\n{text}"
    )

    try:
        client = get_client()

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=512,
                automatic_function_calling=(
                    types.AutomaticFunctionCallingConfig(disable=True)
                ),
            ),
        )

        result = (response.text or "").strip()

        if not result:
            raise RuntimeError("Gemini returned an empty response.")

        logger.info(
            "Rephrase successful | " "output_chars=%d",
            len(result),
        )

        return result

    except Exception:
        logger.exception("Rephrase request failed")
        raise
