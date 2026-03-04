import io
import zipfile
import uuid
from typing import Optional

from app.core.config import settings
from app.core.storage import get_s3_client, get_s3_client_public

TEMPLATES = {
    "classic": {
        "bg": "#ffffff",
        "title_color": "#1a1a1a",
        "body_color": "#444444",
        "footer_color": "#888888",
        "font_family": "'Georgia', serif",
        "title_size": "48px",
        "body_size": "32px",
        "accent_color": "#2563eb",
    },
    "bold": {
        "bg": "#0f0f0f",
        "title_color": "#ffffff",
        "body_color": "#e0e0e0",
        "footer_color": "#aaaaaa",
        "font_family": "'Arial Black', sans-serif",
        "title_size": "56px",
        "body_size": "34px",
        "accent_color": "#f59e0b",
    },
    "minimal": {
        "bg": "#f8f8f6",
        "title_color": "#222222",
        "body_color": "#555555",
        "footer_color": "#999999",
        "font_family": "'Helvetica Neue', Helvetica, sans-serif",
        "title_size": "44px",
        "body_size": "30px",
        "accent_color": "#10b981",
    },
}


def build_slide_html(slide, design: dict, slide_number: int, total: int) -> str:
    template_name = design.get("template", "classic")
    tpl = TEMPLATES.get(template_name, TEMPLATES["classic"])

    bg_color = design.get("bg_color", tpl["bg"])
    bg_image_url = design.get("bg_image_url")
    darkening = design.get("darkening", 0.0)
    padding = design.get("padding", 40)
    align_h = design.get("align_h", "center")
    align_v = design.get("align_v", "center")
    show_header = design.get("show_header", False)
    header_text = design.get("header_text", "")
    show_footer = design.get("show_footer", False)
    footer_text = design.get("footer_text", "")

    justify_map = {"left": "flex-start", "center": "center", "right": "flex-end"}
    align_map = {"top": "flex-start", "center": "center", "bottom": "flex-end"}
    text_align_map = {"left": "left", "center": "center", "right": "right"}

    bg_style = f"background-color: {bg_color};"
    if bg_image_url:
        bg_style = f"background-image: url('{bg_image_url}'); background-size: cover; background-position: center;"

    overlay = ""
    if darkening > 0 and bg_image_url:
        overlay = f'<div style="position:absolute;inset:0;background:rgba(0,0,0,{darkening});"></div>'

    header_html = ""
    if show_header and header_text:
        header_html = f"""
        <div style="
            position: absolute;
            top: {padding}px;
            left: {padding}px;
            right: {padding}px;
            font-family: {tpl['font_family']};
            font-size: 22px;
            color: {tpl['footer_color']};
            text-align: {text_align_map[align_h]};
            z-index: 10;
        ">{header_text}</div>"""

    footer_html = ""
    if show_footer and footer_text:
        footer_html = f"""
        <div style="
            position: absolute;
            bottom: {padding}px;
            left: {padding}px;
            right: {padding}px;
            font-family: {tpl['font_family']};
            font-size: 22px;
            color: {tpl['footer_color']};
            text-align: {text_align_map[align_h]};
            z-index: 10;
        ">{footer_text}</div>"""

    slide_counter = f"""
    <div style="
        position: absolute;
        top: {padding}px;
        right: {padding}px;
        font-family: {tpl['font_family']};
        font-size: 20px;
        color: {tpl['footer_color']};
        z-index: 10;
    ">{slide_number}/{total}</div>"""

    footer_cta_html = ""
    if slide.footer_cta:
        footer_cta_html = f"""
        <div style="
            margin-top: 32px;
            font-family: {tpl['font_family']};
            font-size: 26px;
            color: {tpl['accent_color']};
            font-weight: bold;
        ">{slide.footer_cta}</div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1350px; overflow: hidden; }}
</style>
</head>
<body>
<div style="
    position: relative;
    width: 1080px;
    height: 1350px;
    {bg_style}
    display: flex;
    flex-direction: column;
    justify-content: {align_map[align_v]};
    align-items: {justify_map[align_h]};
">
{overlay}
{header_html}
{slide_counter}
<div style="
    position: relative;
    z-index: 5;
    padding: {padding}px;
    width: 100%;
    text-align: {text_align_map[align_h]};
    max-width: 960px;
">
    <div style="
        font-family: {tpl['font_family']};
        font-size: {tpl['title_size']};
        font-weight: bold;
        color: {tpl['title_color']};
        line-height: 1.2;
        margin-bottom: 32px;
    ">{slide.title}</div>
    <div style="
        font-family: {tpl['font_family']};
        font-size: {tpl['body_size']};
        color: {tpl['body_color']};
        line-height: 1.6;
    ">{slide.body}</div>
    {footer_cta_html}
</div>
{footer_html}
</div>
</body>
</html>"""


async def render_slides_to_zip(carousel, slides: list) -> str:
    """Render all slides to PNG, pack into ZIP, upload to MinIO, return presigned URL."""
    from playwright.async_api import async_playwright

    png_buffers = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        for i, slide in enumerate(slides):
            html = build_slide_html(slide, carousel.design or {}, i + 1, len(slides))
            await page.set_content(html, wait_until="networkidle")
            png_bytes = await page.screenshot(type="png", clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
            png_buffers.append(png_bytes)
        await browser.close()

    # Build ZIP in memory
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for idx, png in enumerate(png_buffers, 1):
            zf.writestr(f"slide_{idx:02d}.png", png)
    zip_buf.seek(0)

    # Upload to MinIO using the internal endpoint
    key = f"exports/{carousel.id}/{uuid.uuid4()}.zip"
    async with get_s3_client() as s3:
        await s3.put_object(
            Bucket=settings.minio_bucket,
            Key=key,
            Body=zip_buf.getvalue(),
            ContentType="application/zip",
        )

    # Generate presigned URL using the public endpoint so the signature matches what the browser sends
    async with get_s3_client_public() as s3:
        url = await s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.minio_bucket, "Key": key},
            ExpiresIn=3600,
        )

    return url
