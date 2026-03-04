import json
import re
import httpx

from app.core.config import settings
from app.schemas.slide import SlideGeneratedItem

LANGUAGE_NAMES = {"ru": "Russian", "en": "English", "fr": "French"}


def _extract_source_text(carousel) -> str:
    payload = carousel.source_payload or {}
    if carousel.source_type == "text":
        return payload.get("text", "")
    elif carousel.source_type == "video":
        return f"Video URL: {payload.get('video_url', '')}. {payload.get('notes', '')}"
    elif carousel.source_type == "links":
        links = payload.get("links", [])
        notes = payload.get("notes", "")
        return f"Links: {', '.join(links)}. Notes: {notes}"
    return ""


def estimate_tokens(carousel) -> int:
    fmt = carousel.format or {}
    slides_count = fmt.get("slides_count", 8)
    source_text = _extract_source_text(carousel)
    return 200 + min(len(source_text), 2000) + slides_count * 80


async def generate_slides(carousel) -> tuple[list[SlideGeneratedItem], int]:
    fmt = carousel.format or {}
    slides_count = fmt.get("slides_count", 8)
    language = fmt.get("language", "ru")
    style_hint = fmt.get("style_hint", "")
    source_text = _extract_source_text(carousel)
    lang_name = LANGUAGE_NAMES.get(language, "Russian")

    style_section = ""
    if style_hint:
        style_section = f"\n\nStyle example (match this writing style and tone):\n{style_hint[:500]}"

    prompt = f"""Create exactly {slides_count} Instagram carousel slides in {lang_name}.

Source material:
{source_text[:3000]}{style_section}

Return a JSON array with exactly {slides_count} objects. Each object must have:
- "order": integer starting from 1
- "title": string, max 60 characters, catchy slide headline
- "body": string, max 280 characters, main slide content
- "footer_cta": string max 80 characters OR null

Output ONLY the JSON array, no markdown, no explanation."""

    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.llm_model,
        "messages": [
            {
                "role": "system",
                "content": "You are a social media content creator specializing in Instagram carousels. Always respond with valid JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 4096,
        "temperature": 0.7,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        for attempt in range(2):
            resp = await client.post(settings.llm_base_url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

            raw = data["choices"][0]["message"]["content"].strip()
            # strip markdown code fences if present
            raw = re.sub(r"^```(?:json)?\n?", "", raw)
            raw = re.sub(r"\n?```$", "", raw)

            tokens_used = data.get("usage", {}).get("total_tokens", 0)

            try:
                parsed = json.loads(raw)
                if not isinstance(parsed, list) or len(parsed) != slides_count:
                    raise ValueError(f"Expected {slides_count} slides, got {len(parsed) if isinstance(parsed, list) else type(parsed).__name__}")
                slides = [SlideGeneratedItem(**item) for item in parsed]
                return slides, tokens_used
            except Exception as e:
                if attempt == 1:
                    raise ValueError(f"LLM returned invalid JSON after 2 attempts: {e}\nRaw: {raw[:500]}")
                continue

    raise ValueError("Generation failed")
