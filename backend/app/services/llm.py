import asyncio
import json
import re
import logging
import httpx

from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, CouldNotRetrieveTranscript
from bs4 import BeautifulSoup

from app.core.config import settings
from app.schemas.slide import SlideGeneratedItem

logger = logging.getLogger(__name__)

LANGUAGE_NAMES = {"ru": "Russian", "en": "English", "fr": "French"}

_YT_ID_RE = re.compile(
    r"(?:youtube\.com/(?:watch\?v=|shorts/|embed/)|youtu\.be/)([\w-]{11})"
)


def _extract_youtube_id(url: str) -> str | None:
    m = _YT_ID_RE.search(url)
    return m.group(1) if m else None


def _fetch_youtube_transcript(video_id: str) -> str:
    """Fetch transcript synchronously (youtube-transcript-api is sync)."""
    try:
        ytt = YouTubeTranscriptApi()
        # Try fetching in any available language
        transcript = ytt.fetch(video_id)
        text = " ".join(entry.text for entry in transcript)
        return text[:6000]
    except (NoTranscriptFound, TranscriptsDisabled, CouldNotRetrieveTranscript):
        # Fall back: list all transcripts and grab the first available
        try:
            ytt = YouTubeTranscriptApi()
            listing = ytt.list(video_id)
            t = next(iter(listing))
            fetched = t.fetch()
            text = " ".join(e.text for e in fetched)
            return text[:6000]
        except Exception as e:
            logger.warning("YouTube transcript unavailable for %s: %s", video_id, e)
            return ""
    except Exception as e:
        logger.warning("YouTube transcript fetch failed for %s: %s", video_id, e)
        return ""


async def _fetch_url_text(url: str, client: httpx.AsyncClient) -> str:
    """Fetch a URL and return cleaned plain text (max 3000 chars)."""
    try:
        resp = await client.get(
            url,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (compatible; CarouselGen/1.0)"},
            timeout=15.0,
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove noise tags
        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        # Collapse whitespace
        text = re.sub(r"\s+", " ", text).strip()
        return text[:4000]
    except Exception as e:
        logger.warning("Failed to fetch URL %s: %s", url, e)
        return ""


async def _build_source_text(carousel) -> str:
    payload = carousel.source_payload or {}

    if carousel.source_type == "text":
        return payload.get("text", "")

    if carousel.source_type == "video":
        video_url = payload.get("video_url", "")
        notes = payload.get("notes", "")
        video_id = _extract_youtube_id(video_url)
        if video_id:
            transcript = await asyncio.get_event_loop().run_in_executor(
                None, _fetch_youtube_transcript, video_id
            )
            if transcript:
                prefix = f"[YouTube transcript for {video_url}]\n\n"
                suffix = f"\n\nAdditional notes: {notes}" if notes else ""
                return prefix + transcript + suffix
        # No transcript — fall back to URL + notes
        return f"Video URL: {video_url}. Notes: {notes}"

    if carousel.source_type == "links":
        links = payload.get("links", [])
        notes = payload.get("notes", "")
        parts = []
        async with httpx.AsyncClient() as client:
            for url in links[:5]:  # cap at 5 URLs
                text = await _fetch_url_text(url, client)
                if text:
                    parts.append(f"[Content from {url}]\n{text}")
        if parts:
            suffix = f"\n\nAdditional notes: {notes}" if notes else ""
            return "\n\n---\n\n".join(parts) + suffix
        # Fallback if all fetches failed
        return f"Links: {', '.join(links)}. Notes: {notes}"

    return ""


def estimate_tokens(carousel) -> int:
    fmt = carousel.format or {}
    slides_count = fmt.get("slides_count", 8)
    payload = carousel.source_payload or {}
    if carousel.source_type == "text":
        source_len = len(payload.get("text", ""))
    else:
        source_len = 2000  # estimate for fetched content
    return 200 + min(source_len, 4000) + slides_count * 80


async def generate_slides(carousel) -> tuple[list[SlideGeneratedItem], int]:
    fmt = carousel.format or {}
    slides_count = fmt.get("slides_count", 8)
    language = fmt.get("language", "ru")
    style_hint = fmt.get("style_hint", "")
    source_text = await _build_source_text(carousel)
    lang_name = LANGUAGE_NAMES.get(language, "Russian")

    style_section = ""
    if style_hint:
        style_section = f"\n\nStyle example (match this writing style and tone):\n{style_hint[:500]}"

    prompt = f"""Create exactly {slides_count} Instagram carousel slides in {lang_name}.

Source material:
{source_text[:5000]}{style_section}

Return a JSON array with exactly {slides_count} objects. Each object must have:
- "order": integer starting from 1
- "title": string, max 60 characters, catchy slide headline
- "body": string, max 280 characters, main slide content
- "footer_cta": string max 80 characters OR null — use null for most slides; only add a CTA on the last slide (e.g. "Save this post ↓", "Follow for more", "Share with someone who needs this")

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
