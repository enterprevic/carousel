import io
import re
import zipfile
import uuid
import base64
from html import escape as _esc
from pathlib import Path
from typing import Optional

from app.core.config import settings
from app.core.storage import get_s3_client, get_s3_client_public

_FONTS_DIR = Path(__file__).parent.parent / "fonts"


def _font_b64(filename: str) -> str:
    path = _FONTS_DIR / filename
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()


def _build_font_face_css() -> str:
    """Build @font-face declarations from locally-bundled TTF files."""
    fonts = [
        ("Roboto Condensed", "RobotoCondensed-Regular.ttf", 400),
        ("Roboto Condensed", "RobotoCondensed-Bold.ttf",    700),
        ("Fredoka",          "Fredoka-Regular.ttf",          400),
        ("Fredoka",          "Fredoka-Bold.ttf",             700),
        ("Jost",             "Jost-Regular.ttf",             400),
        ("Jost",             "Jost-Bold.ttf",                700),
        ("Caveat",           "Caveat-Regular.ttf",           400),
        ("Caveat",           "Caveat-Bold.ttf",              700),
        ("Space Mono",       "SpaceMono-Regular.ttf",        400),
        ("Space Mono",       "SpaceMono-Bold.ttf",           700),
        ("Merriweather",     "Merriweather-Regular.ttf",     400),
        ("Merriweather",     "Merriweather-Bold.ttf",        700),
    ]
    css = []
    for family, filename, weight in fonts:
        b64 = _font_b64(filename)
        if b64:
            css.append(
                f"@font-face {{\n"
                f"  font-family: '{family}';\n"
                f"  font-weight: {weight};\n"
                f"  src: url(data:font/truetype;base64,{b64}) format('truetype');\n"
                f"}}"
            )
    return "\n".join(css)


_FONT_FACE_CSS = _build_font_face_css()

DIMENSIONS = {
    "4:5":  (1080, 1350),
    "9:16": (1080, 1920),
    "1:1":  (1080, 1080),
}

TEMPLATES = {
    "bright": {
        "bg": "#fff7ed",
        "title_color": "#1c1917",
        "body_color": "#44403c",
        "footer_color": "#78716c",
        "font_family": "'Roboto Condensed', Arial, sans-serif",
        "title_size": "48px",
        "body_size": "32px",
        "accent_color": "#f97316",
    },
    "classic": {
        "bg": "#ffffff",
        "title_color": "#1a1a1a",
        "body_color": "#444444",
        "footer_color": "#888888",
        "font_family": "'Times New Roman', Times, serif",
        "title_size": "48px",
        "body_size": "32px",
        "accent_color": "#2563eb",
    },
    "comic": {
        "bg": "#fef08a",
        "title_color": "#18181b",
        "body_color": "#3f3f46",
        "footer_color": "#52525b",
        "font_family": "'Fredoka', Arial, sans-serif",
        "title_size": "54px",
        "body_size": "32px",
        "accent_color": "#7c3aed",
    },
    "elegant": {
        "bg": "#0f172a",
        "title_color": "#f8fafc",
        "body_color": "#cbd5e1",
        "footer_color": "#94a3b8",
        "font_family": "'Times New Roman', Times, serif",
        "title_size": "48px",
        "body_size": "30px",
        "accent_color": "#d4af37",
    },
    "minimal": {
        "bg": "#f8f8f6",
        "title_color": "#222222",
        "body_color": "#555555",
        "footer_color": "#999999",
        "font_family": "'Jost', Arial, sans-serif",
        "title_size": "44px",
        "body_size": "30px",
        "accent_color": "#10b981",
    },
    "notes": {
        "bg": "#fefce8",
        "title_color": "#422006",
        "body_color": "#78350f",
        "footer_color": "#92400e",
        "font_family": "'Caveat', Georgia, cursive",
        "title_size": "54px",
        "body_size": "36px",
        "accent_color": "#d97706",
    },
    "powerful": {
        "bg": "#09090b",
        "title_color": "#fafafa",
        "body_color": "#a1a1aa",
        "footer_color": "#71717a",
        "font_family": "'Space Mono', 'Courier New', monospace",
        "title_size": "56px",
        "body_size": "34px",
        "accent_color": "#ef4444",
    },
}

# Maps frontend font keys to CSS font-family values (web-safe, no Google Fonts needed server-side)
FONT_FAMILIES = {
    "system":       "Arial, Helvetica, sans-serif",
    "playfair":     "Georgia, 'Times New Roman', serif",
    "oswald":       "'Arial Narrow', Arial, sans-serif",
    "montserrat":   "Arial, Helvetica, sans-serif",
    "opensans":     "Arial, Helvetica, sans-serif",
    "lato":         "Arial, Helvetica, sans-serif",
    "merriweather": "Georgia, 'Times New Roman', serif",
    "georgia":      "Georgia, 'Times New Roman', serif",
}


def _render_inline_markup(text: str, accent_color: str) -> str:
    """Mirror the frontend renderInlineMarkup: ==text== → highlight span, **text** → bold span."""
    escaped = _esc(text)
    # ==#bg|#fg|text== → custom-color highlight
    escaped = re.sub(
        r'==(#[0-9a-fA-F]{3,8})\|(#[0-9a-fA-F]{3,8})\|(.+?)==',
        lambda m: (
            f'<span style="background-color:{m.group(1)};color:{m.group(2)};'
            f'border-radius:3px;padding:0 4px;'
            f'-webkit-box-decoration-break:clone;box-decoration-break:clone;">'
            f'{m.group(3)}</span>'
        ),
        escaped,
    )
    # ==text== → accent-color highlight
    escaped = re.sub(
        r'==(.+?)==',
        lambda m: (
            f'<span style="background-color:{accent_color};color:#fff;'
            f'border-radius:3px;padding:0 4px;'
            f'-webkit-box-decoration-break:clone;box-decoration-break:clone;">'
            f'{m.group(1)}</span>'
        ),
        escaped,
    )
    # **text** → bold
    escaped = re.sub(
        r'\*\*(.+?)\*\*',
        lambda m: f'<span style="font-weight:700">{m.group(1)}</span>',
        escaped,
    )
    return escaped


def _internalize_url(url: Optional[str]) -> Optional[str]:
    """Replace public MinIO host with internal docker host for server-side Playwright rendering."""
    if not url:
        return url
    public_base = settings.minio_public_url.rstrip("/")
    internal_base = f"{'https' if settings.minio_secure else 'http'}://{settings.minio_endpoint}"
    if url.startswith(public_base):
        return url.replace(public_base, internal_base, 1)
    return url


def build_slide_html(slide, design: dict, slide_number: int, total: int, width: int = 1080, height: int = 1350) -> str:
    # Per-slide overrides take precedence over carousel-level design
    overrides: dict = getattr(slide, "overrides", None) or {}

    # Resolve template (slide override > carousel design)
    template_name = overrides.get("template") or design.get("template", "classic")
    tpl = TEMPLATES.get(template_name, TEMPLATES["classic"])

    title_font_key = design.get("title_font", "system")
    body_font_key = design.get("body_font", "system")
    # "system" means "use the template's own font"; only override when a specific font is chosen
    title_font_family = tpl["font_family"] if title_font_key == "system" else FONT_FAMILIES.get(title_font_key, tpl["font_family"])
    body_font_family = tpl["font_family"] if body_font_key == "system" else FONT_FAMILIES.get(body_font_key, tpl["font_family"])

    def _ov(key, default=None):
        """Return override value if key is present, else design value, else default."""
        if key in overrides:
            return overrides[key]
        return design.get(key, default)

    # Scale factor: all px sizes were authored for 1080-wide canvas; scale proportionally
    scale = width / 1080.0

    bg_color = _ov("bg_color") or tpl["bg"]
    # Internalize image URLs for Playwright (which runs inside Docker and uses minio:9000)
    raw_bg_image = _ov("bg_image_url")
    bg_image_url = _internalize_url(raw_bg_image)
    darkening = _ov("darkening", 0.0)
    padding = round(_ov("padding", 40) * scale)
    align_h = _ov("align_h") or "center"
    align_v = _ov("align_v") or "center"
    show_header = _ov("show_header", False)
    header_text = _ov("header_text", "")
    show_footer = _ov("show_footer", False)
    footer_text = _ov("footer_text", "")
    accent_color = _ov("accent_color") or tpl["accent_color"]
    pattern = _ov("pattern", "none")
    pattern_color = _ov("pattern_color", "#000000")
    pattern_opacity = _ov("pattern_opacity", 0.06)
    title_highlight = _ov("title_highlight")

    justify_map = {"left": "flex-start", "center": "center", "right": "flex-end"}
    align_map = {"top": "flex-start", "center": "center", "bottom": "flex-end", "spread": "space-between"}
    text_align_map = {"left": "left", "center": "center", "right": "right"}

    bg_style = f"background-color: {bg_color};"
    if bg_image_url:
        bg_style = f"background-image: url('{bg_image_url}'); background-size: cover; background-position: center;"

    overlay = ""
    if darkening > 0 and bg_image_url:
        overlay = f'<div style="position:absolute;inset:0;background:rgba(0,0,0,{darkening});"></div>'

    pattern_overlay = ""
    if pattern and pattern != "none":
        svg_map = {
            "dots1": f"<svg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'><circle cx='2' cy='2' r='1.5' fill='{pattern_color}' fill-opacity='{pattern_opacity}'/></svg>",
            "dots2": f"<svg width='16' height='16' viewBox='0 0 16 16' xmlns='http://www.w3.org/2000/svg'><circle cx='2' cy='2' r='2' fill='{pattern_color}' fill-opacity='{pattern_opacity}'/></svg>",
            "dots3": f"<svg width='30' height='30' viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'><circle cx='3' cy='3' r='3' fill='{pattern_color}' fill-opacity='{pattern_opacity}'/></svg>",
            "grid":  f"<svg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><path d='M24 0H0v1h24V0zm0 23H0v1h24v-1zM1 0v24h1V0H1zm22 0v24h1V0h-1z' fill='{pattern_color}' fill-opacity='{pattern_opacity}'/></svg>",
            "lines": f"<svg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'><line x1='0' y1='10' x2='20' y2='10' stroke='{pattern_color}' stroke-opacity='{pattern_opacity}' stroke-width='1'/></svg>",
            "cells": f"<svg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'><path d='M0 20h40M20 0v40' stroke='{pattern_color}' stroke-opacity='{pattern_opacity}' stroke-width='0.8'/></svg>",
            "blobs": f"<svg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'><path d='M28 14c7 -3 16 1 18 8s-3 16 -10 19s-16 -1 -18 -9s3 -15 10 -18z' fill='{pattern_color}' fill-opacity='{pattern_opacity}'/><path d='M85 52c8 2 14 10 12 18s-11 13 -19 11s-13 -11 -11 -19s10 -12 18 -10z' fill='{pattern_color}' fill-opacity='{pattern_opacity}'/><path d='M22 82c6 -4 15 -2 19 5s1 16 -6 20s-15 1 -19 -6s0 -15 6 -19z' fill='{pattern_color}' fill-opacity='{pattern_opacity}'/><path d='M95 10c5 3 7 10 4 16s-10 9 -16 6s-7 -10 -4 -16s10 -9 16 -6z' fill='{pattern_color}' fill-opacity='{pattern_opacity}'/><path d='M58 90c6 -2 12 3 13 9s-3 12 -9 13s-12 -3 -13 -10s3 -10 9 -12z' fill='{pattern_color}' fill-opacity='{pattern_opacity}'/></svg>",
        }
        if pattern in svg_map:
            svg_b64 = base64.b64encode(svg_map[pattern].encode()).decode()
            pattern_overlay = f'<div style="position:absolute;inset:0;background-image:url(\'data:image/svg+xml;base64,{svg_b64}\');background-repeat:repeat;z-index:2;pointer-events:none;"></div>'

    header_html = ""
    if show_header and header_text:
        header_html = f"""
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            padding: {padding}px {padding}px 0;
            font-family: {tpl['font_family']};
            font-size: {round(22 * scale)}px;
            color: {tpl['footer_color']};
            text-align: {text_align_map[align_h]};
            z-index: 10;
        ">{_esc(header_text)}</div>"""

    footer_html = ""
    if show_footer and footer_text:
        footer_html = f"""
        <div style="
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 0 {padding}px {padding}px;
            font-family: {tpl['font_family']};
            font-size: {round(22 * scale)}px;
            color: {tpl['footer_color']};
            text-align: {text_align_map[align_h]};
            z-index: 10;
        ">{_esc(footer_text)}</div>"""

    slide_counter = f"""
    <div style="
        position: absolute;
        top: 0;
        right: 0;
        padding: {padding}px {padding}px 0 0;
        font-family: {tpl['font_family']};
        font-size: {round(20 * scale)}px;
        color: {tpl['footer_color']};
        z-index: 10;
    ">{slide_number}/{total}</div>"""

    footer_cta_html = ""
    if slide.footer_cta:
        footer_cta_html = f"""
        <div style="
            margin-top: {round(32 * scale)}px;
            font-family: {body_font_family};
            font-size: {round(26 * scale)}px;
            color: {accent_color};
            font-weight: bold;
        ">{_esc(slide.footer_cta)}</div>"""

    # Scale template font sizes proportionally to canvas width
    def _scale_px(css_px: str) -> str:
        px = int(css_px.replace("px", ""))
        return f"{round(px * scale)}px"

    title_size_scaled = _scale_px(tpl["title_size"])
    body_size_scaled  = _scale_px(tpl["body_size"])
    title_margin_bottom = round(32 * scale)

    title_style = f"font-family: {title_font_family}; font-size: {title_size_scaled}; font-weight: bold; color: {tpl['title_color']}; line-height: 1.2; margin-bottom: {title_margin_bottom}px;"
    if title_highlight:
        title_style += f" background-color: {title_highlight}; padding: 0 8px; border-radius: 4px; display: inline; -webkit-box-decoration-break: clone; box-decoration-break: clone;"

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
{_FONT_FACE_CSS}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: {width}px; height: {height}px; overflow: hidden; }}
</style>
</head>
<body>
<div style="
    position: relative;
    width: {width}px;
    height: {height}px;
    {bg_style}
    display: flex;
    flex-direction: column;
    justify-content: {align_map[align_v]};
    align-items: {justify_map[align_h]};
    padding: {padding}px;
    box-sizing: border-box;
">
{overlay}
{pattern_overlay}
{header_html}
{slide_counter}
<div style="
    position: relative;
    z-index: 5;
    width: 100%;
    text-align: {text_align_map[align_h]};
">
    <div style="{title_style}">{_render_inline_markup(slide.title, accent_color)}</div>
    <div style="
        font-family: {body_font_family};
        font-size: {body_size_scaled};
        color: {tpl['body_color']};
        line-height: 1.6;
    ">{_render_inline_markup(slide.body, accent_color)}</div>
    {footer_cta_html}
</div>
{footer_html}
</div>
</body>
</html>"""


async def render_slides_to_zip(carousel, slides: list) -> tuple[str, list[str]]:
    """Render all slides to PNG, upload individually and as ZIP. Returns (zip_url, [slide_urls])."""
    from playwright.async_api import async_playwright

    design = carousel.design or {}
    w, h = DIMENSIONS.get(design.get("aspect_ratio", "4:5"), (1080, 1350))
    export_id = uuid.uuid4()

    png_buffers = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        for i, slide in enumerate(slides):
            html = build_slide_html(slide, design, i + 1, len(slides), width=w, height=h)
            await page.set_content(html, wait_until="load")
            png_bytes = await page.screenshot(type="png", clip={"x": 0, "y": 0, "width": w, "height": h})
            png_buffers.append(png_bytes)
        await browser.close()

    # Build ZIP in memory
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for idx, png in enumerate(png_buffers, 1):
            zf.writestr(f"slide_{idx:02d}.png", png)
    zip_buf.seek(0)

    # Upload ZIP and individual PNGs to MinIO
    zip_key = f"exports/{carousel.id}/{export_id}/slides.zip"
    slide_keys = [f"exports/{carousel.id}/{export_id}/slide_{idx:02d}.png" for idx in range(1, len(png_buffers) + 1)]

    async with get_s3_client() as s3:
        await s3.put_object(
            Bucket=settings.minio_bucket,
            Key=zip_key,
            Body=zip_buf.getvalue(),
            ContentType="application/zip",
        )
        for key, png in zip(slide_keys, png_buffers):
            await s3.put_object(
                Bucket=settings.minio_bucket,
                Key=key,
                Body=png,
                ContentType="image/png",
            )

    # Generate presigned URLs using the public endpoint
    async with get_s3_client_public() as s3:
        zip_url = await s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.minio_bucket, "Key": zip_key},
            ExpiresIn=86400,
        )
        slide_urls = []
        for key in slide_keys:
            url = await s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.minio_bucket, "Key": key},
                ExpiresIn=86400,
            )
            slide_urls.append(url)

    return zip_url, slide_urls
