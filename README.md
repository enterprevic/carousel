# Carousel Generator

An Instagram carousel generator. Create carousels from text or video, configure format, generate slides with AI, edit in a visual editor, and export as PNG ZIP.

## Stack

| Layer | Tech |
|-------|------|
| Backend | Python 3.12 + FastAPI + SQLAlchemy (async) + Alembic |
| Database | PostgreSQL 16 |
| Storage | MinIO (S3-compatible) |
| LLM | Groq API (`llama-3.3-70b-versatile`) via httpx |
| Export | Playwright (headless Chromium → PNG) |
| Frontend | Nuxt 3 + Vue 3 + Tailwind CSS + Pinia |
| Infra | Docker Compose |

---

## Quick Start

### Prerequisites
- Docker + Docker Compose
- Groq API key (free at [console.groq.com](https://console.groq.com))

### 1. Clone and configure

```bash
git clone <repo>
cd generator
cp .env.example .env
# Edit .env and set your LLM_API_KEY=gsk_...
```

### 2. Start everything

```bash
docker-compose up --build
```

This will:
- Start PostgreSQL
- Start MinIO
- Run Alembic migrations
- Start FastAPI backend on **http://localhost:8000**
- Start Nuxt frontend on **http://localhost:3000**

### 3. Open the app

Visit **http://localhost:3000**

---

## API Reference

### Carousels

#### `GET /carousels`
List all carousels. Optional query params: `?status=draft|generating|ready|failed`, `?lang=en|ru|fr`

**Response:** array of carousel objects

#### `GET /carousels/{id}`
Get a single carousel.

#### `POST /carousels`
Create a new carousel.

```json
{
  "title": "5 Python Tips",
  "source_type": "text",
  "source_payload": { "text": "..." },
  "format": {
    "slides_count": 6,
    "language": "en",
    "style_hint": "Keep it punchy and actionable."
  }
}
```

`source_type`: `text` | `video` | `links`
`slides_count`: 6–10
`language`: `en` | `ru` | `fr`

#### `PATCH /carousels/{id}`
Update carousel title, format, or design (partial update).

#### `PATCH /carousels/{id}/design`
Update only the design settings.

```json
{
  "template": "elegant",
  "bg_color": "#0f172a",
  "bg_image_url": null,
  "darkening": 0.3,
  "padding": 50,
  "align_h": "left",
  "align_v": "center",
  "aspect_ratio": "9:16",
  "accent_color": "#d4af37",
  "pattern": "dots1",
  "pattern_color": "#ffffff",
  "pattern_opacity": 0.08,
  "title_font": "playfair",
  "body_font": "opensans",
  "title_highlight": "#f97316",
  "show_header": false,
  "header_text": "",
  "show_footer": true,
  "footer_text": "Follow for more"
}
```

| Field | Type | Values / Range | Default |
|-------|------|----------------|---------|
| `template` | string | `bright` `classic` `comic` `elegant` `minimal` `notes` `powerful` | `classic` |
| `bg_color` | string | hex color | `#ffffff` |
| `bg_image_url` | string\|null | URL | `null` |
| `darkening` | float | 0.0 – 1.0 | `0.0` |
| `padding` | int | 20 – 80 | `40` |
| `align_h` | string | `left` `center` `right` | `center` |
| `align_v` | string | `top` `center` `bottom` | `center` |
| `aspect_ratio` | string | `4:5` `9:16` `1:1` | `4:5` |
| `accent_color` | string\|null | hex color | `null` |
| `pattern` | string | `none` `dots1` `dots2` `dots3` `grid` `lines` `cells` `blobs` | `none` |
| `pattern_color` | string | hex color | `#000000` |
| `pattern_opacity` | float | 0.0 – 0.5 | `0.06` |
| `title_font` | string | `system` `playfair` `oswald` `montserrat` `opensans` `lato` `merriweather` `georgia` | `system` |
| `body_font` | string | same as title_font | `system` |
| `title_highlight` | string\|null | hex color | `null` |
| `show_header` | bool | | `false` |
| `header_text` | string | | `""` |
| `show_footer` | bool | | `false` |
| `footer_text` | string | | `""` |

---

### Slides

#### `GET /carousels/{id}/slides`
Get all slides for a carousel (ordered).

**Response:**
```json
[
  {
    "id": "...",
    "carousel_id": "...",
    "order": 1,
    "title": "Slide Title",
    "body": "Slide body text.",
    "footer_cta": "Follow for more",
    "overrides": {},
    "created_at": "...",
    "updated_at": "..."
  }
]
```

#### `PATCH /carousels/{id}/slides/{slide_id}`
Update a slide's content or per-slide design overrides.

```json
{
  "title": "New Title",
  "body": "Updated body text.",
  "footer_cta": "Save this post",
  "overrides": {
    "bg_color": "#1a1a2e",
    "bg_image_url": "http://...",
    "darkening": 0.5
  }
}
```

All fields optional. `overrides` fields override the carousel-level design for that slide only.

---

### Generations

#### `POST /generations`
Trigger AI slide generation for a carousel. Runs in the background.

```json
{ "carousel_id": "<id>" }
```

**Response:**
```json
{
  "id": "...",
  "carousel_id": "...",
  "status": "queued",
  "estimated_tokens": 650,
  "tokens_used": null,
  "error": null,
  "created_at": "...",
  "updated_at": "..."
}
```

#### `GET /generations/{id}`
Poll generation status.

`status`: `queued` → `running` → `done` | `failed`

---

### Exports

#### `POST /exports`
Start a PNG export for a carousel. Runs in the background.

```json
{ "carousel_id": "<id>" }
```

#### `GET /exports/{id}`
Poll export status.

```json
{
  "id": "...",
  "carousel_id": "...",
  "status": "done",
  "file_url": "http://localhost:9000/carousel-assets/exports/.../slides.zip",
  "created_at": "..."
}
```

`status`: `queued` → `running` → `done` | `failed`
`file_url` is a presigned URL valid for 1 hour.

---

### Assets

#### `POST /assets/upload`
Upload an image to use as a slide background.

```bash
curl -X POST http://localhost:8000/assets/upload \
  -F "file=@/path/to/image.jpg"
```

Accepted types: `jpeg`, `png`, `webp`, `gif`. Max size: 10 MB.

**Response:**
```json
{ "url": "http://localhost:9000/carousel-assets/assets/...jpg" }
```

---

## Full Workflow Example

```bash
# 1. Create carousel
curl -X POST http://localhost:8000/carousels \
  -H "Content-Type: application/json" \
  -d '{"title":"5 Python Tips","source_type":"text","source_payload":{"text":"Python is great for automation..."},"format":{"slides_count":6,"language":"en","style_hint":"punchy and actionable"}}'
# → {"id": "abc-123", ...}

# 2. Generate slides
curl -X POST http://localhost:8000/generations \
  -H "Content-Type: application/json" \
  -d '{"carousel_id": "abc-123"}'
# → {"id": "gen-456", "status": "queued", ...}

# 3. Poll until done
curl http://localhost:8000/generations/gen-456
# → {"status": "done", "tokens_used": 712}

# 4. (Optional) Update design
curl -X PATCH http://localhost:8000/carousels/abc-123/design \
  -H "Content-Type: application/json" \
  -d '{"template":"powerful","aspect_ratio":"9:16","pattern":"dots1"}'

# 5. Export
curl -X POST http://localhost:8000/exports \
  -H "Content-Type: application/json" \
  -d '{"carousel_id": "abc-123"}'
# → {"id": "exp-789", "status": "queued"}

# 6. Poll until done
curl http://localhost:8000/exports/exp-789
# → {"status": "done", "file_url": "http://..."}

# 7. Download
curl -L "<file_url>" -o slides.zip && unzip slides.zip
# → slide_01.png, slide_02.png, ...
```

---

## Project Structure

```
generator/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # carousels, slides, generations, exports, assets
│   │   ├── core/            # config, database, storage
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # llm.py, export_svc.py, storage_svc.py
│   ├── alembic/             # DB migrations
│   └── requirements.txt
├── frontend/
│   ├── pages/               # index, carousels/new, carousels/[id]/edit
│   ├── components/          # CarouselCard, SlidePreview, DesignPanel, ExportButton
│   ├── composables/         # useCarousels, useGeneration, useExport
│   └── types/               # TypeScript interfaces
├── docker-compose.yml
└── .env.example
```

---

## Features

### Backend
- Async FastAPI with SQLAlchemy 2.0 (asyncpg driver)
- Background tasks for LLM generation and export (FastAPI BackgroundTasks)
- Slide generation via Groq `llama-3.3-70b-versatile` with JSON validation + 1 retry
- Export: Playwright renders each slide as HTML → screenshot → PNG → ZIP → MinIO
- Variable export dimensions based on selected aspect ratio
- Bundled TTF fonts for consistent rendering across environments
- MinIO for asset storage with public read policy

### Frontend
- Nuxt 3 + Vue 3 Composition API + Pinia
- Desktop + mobile responsive layout
- Creation wizard (3 steps: source type → content → format)
- Visual editor with slide thumbnails, text editing, and design panel
- Design auto-saves on change (debounced 800ms)
- Per-slide background image and color overrides

### Design Panel

| Tab | Options |
|-----|---------|
| **Template** | 7 presets: Bright, Classic, Comic, Elegant, Minimal, Notes, Powerful |
| **Background** | Solid color, image upload with URL, darkening overlay slider |
| **Pattern** | 8 overlay patterns: Dots S/M/L, Grid, Lines, Cells, Blobs — with color + opacity controls |
| **Layout** | Padding, horizontal + vertical alignment, aspect ratio (4:5 / 9:16 / 1:1) |
| **Typography** | Title font, body font (8 choices each), accent color override, title highlight color |
| **Header/Footer** | Toggle + text for header and footer |

### Export

| Aspect Ratio | Dimensions | Use Case |
|-------------|------------|----------|
| 4:5 | 1080×1350 px | Instagram Feed (portrait) |
| 9:16 | 1080×1920 px | Stories / Reels |
| 1:1 | 1080×1080 px | Square post |

- Format: PNG (lossless)
- Naming: `slide_01.png`, `slide_02.png`, …
- Delivery: ZIP archive via presigned MinIO URL (1-hour TTL)

---

## Known Limitations

| Area | Limitation |
|------|-----------|
| **Video** | Accepts URL only; no actual video transcription (LLM uses URL + notes as context) |
| **Export speed** | First export is slow (~30-60s) because Playwright launches Chromium. Subsequent exports are faster. |
| **Auth** | No authentication. API is open. |
| **Generation polling** | Frontend polls every 2s via REST. No WebSockets/SSE. |
| **Concurrency** | BackgroundTasks runs in the same process. For production, use Celery + Redis. |

---

## Development (without Docker)

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Set env vars
export DATABASE_URL="postgresql+asyncpg://carousel:carousel@localhost:5432/carousel"
export LLM_API_KEY="gsk_..."
export MINIO_ENDPOINT="localhost:9000"
# ... etc

alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
NUXT_PUBLIC_API_BASE=http://localhost:8000 npm run dev
```

---

## MinIO Console

Access the MinIO web console at **http://localhost:9001**

- Username: `minioadmin`
- Password: `minioadmin`
