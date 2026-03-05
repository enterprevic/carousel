# CarouselGen

AI-powered Instagram carousel generator. Paste text, a YouTube link, or any URL — AI writes the slides, you style and export as high-resolution PNGs.

---

## Stack

| Layer | Tech |
|-------|------|
| Backend | Python 3.12 + FastAPI + SQLAlchemy 2.0 (async) + Alembic |
| Database | PostgreSQL 16 |
| Storage | MinIO (S3-compatible) |
| LLM | Any OpenAI-compatible API (Groq, OpenAI, OpenRouter, Ollama) |
| Export | Playwright headless Chromium → PNG → ZIP |
| Frontend | Nuxt 3 + Vue 3 + Tailwind CSS |
| Auth | JWT + bcrypt (per-user accounts) |
| Infra | Docker Compose |

---

## Quick Start

### Prerequisites
- Docker + Docker Compose
- An LLM API key — Groq is free at [console.groq.com](https://console.groq.com)

### 1. Clone and configure

```bash
git clone <repo>
cd generator
cp .env.example .env
```

Open `.env` and set at minimum:

```env
LLM_API_KEY=gsk_...          # your Groq key (or OpenAI / other)
JWT_SECRET=<random string>   # openssl rand -hex 32
```

### 2. Start everything

```bash
docker-compose up --build
```

Starts PostgreSQL, MinIO, runs Alembic migrations, and launches the backend (port 8000) and frontend (port 3000).

### 3. Open the app

Visit **[http://localhost:3000](http://localhost:3000)**, register an account, and create your first carousel.

---

## Features

### Content Sources
- **Text** — paste any text directly; the AI turns it into slides
- **YouTube video** — paste a video URL; transcripts are auto-fetched (falls back to URL + notes if captions are unavailable)
- **Links** — paste up to 5 URLs; each page is scraped to plain text and fed to the AI

### AI Generation
- Structured slide output: title, body, optional CTA per slide
- Choose slide count (6–12), language (EN / RU / FR), and an optional style hint
- Automatic retry on malformed JSON responses
- Generation history — view past generation runs per carousel

### Visual Editor
- **Live slide preview** — see exactly how your slide will look as you edit
- **Slide list sidebar** — navigate, reorder (up/down), and delete slides
- **Inline text formatting** — select text directly on the slide preview to get a floating toolbar:
  - **Highlight** — wraps selected text in a colored highlight span
  - **Bold** — wraps selected text in bold
  - **Custom highlight colors** — pick background color and text color per highlight via color swatches in the toolbar
- **Title and body editing** with blur-to-save
- **Optional CTA line** per slide (e.g. "Save this post ↓")

### Design System
- **7 templates**: Bright, Classic, Comic, Elegant, Minimal, Notes, Powerful
- **Accent color** — one-click color to unify highlights, CTAs, and emphasis across all slides
- **Background color** — per-carousel custom hex color
- **Background image** — upload a photo for a slide background with adjustable darkening overlay
- **8 overlay patterns**: Dots (S/M/L), Grid, Lines, Cells, Blobs — with custom color and opacity
- **3 aspect ratios**: 4:5 (portrait), 9:16 (stories), 1:1 (square)
- **Horizontal alignment**: left, center, right
- **Vertical alignment**: top, center, bottom
- **Custom padding**: 20–200 px
- **Title font** and **body font**: 10 choices including Playfair, Oswald, Montserrat, Space Mono, Merriweather, and more
- **Title highlight color** — highlight-box style behind the title
- **Header / Footer text** — optional persistent text shown on every slide (e.g. @username)

### Per-slide Overrides
Any design field can be overridden on individual slides independently of the carousel-level design:
- Background color or image
- Template, accent color, title highlight
- Alignment, padding
- Pattern and overlay settings
- Header / footer visibility and text

### Export
- **PNG export** — Playwright renders each slide at full resolution
- Output sizes: 1080×1350 (4:5), 1080×1920 (9:16), 1080×1080 (1:1)
- Slides packed into a ZIP archive and uploaded to MinIO
- Inline markup (highlights, bold) renders correctly in exports

### Account & Data
- Per-user registration and login (JWT, bcrypt)
- All carousels, slides, and assets are scoped to the authenticated user
- Change password from the profile page
- Usage stats: carousel count, generation count, tokens used

---

## LLM Configuration

Configure via `.env`:

| Provider | `LLM_BASE_URL` | `LLM_MODEL` |
|----------|----------------|-------------|
| **Groq** (default) | `https://api.groq.com/openai/v1/chat/completions` | `llama-3.3-70b-versatile` |
| OpenAI | `https://api.openai.com/v1/chat/completions` | `gpt-4o-mini` |
| OpenRouter | `https://openrouter.ai/api/v1/chat/completions` | `meta-llama/llama-3.1-8b-instruct:free` |
| Ollama (local) | `http://host.docker.internal:11434/v1/chat/completions` | `llama3.2` |

---

## API Reference

All endpoints (except `/auth/register`, `/auth/login`, `/health`) require:
```
Authorization: Bearer <token>
```

### Auth

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/register` | Create account `{username, password}` → JWT |
| `POST` | `/auth/login` | Sign in `{username, password}` → JWT |
| `GET` | `/auth/me` | Current user info |
| `POST` | `/auth/password` | Change password `{current_password, new_password}` |
| `GET` | `/auth/me/stats` | Usage stats (carousels, generations, tokens) |

### Carousels

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/carousels` | List your carousels |
| `POST` | `/carousels` | Create a carousel |
| `GET` | `/carousels/{id}` | Get a single carousel |
| `PATCH` | `/carousels/{id}` | Update title / format |
| `PATCH` | `/carousels/{id}/design` | Update design settings |
| `DELETE` | `/carousels/{id}` | Delete carousel and all slides |

**Create carousel body:**
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

| Source type | Payload fields | What the LLM receives |
|-------------|----------------|-----------------------|
| `text` | `text` | The pasted text directly |
| `video` | `video_url`, `notes` | Auto-fetched YouTube transcript + notes; falls back to URL + notes |
| `links` | `links[]`, `notes` | Each URL scraped to plain text (up to 5 URLs, 4000 chars each) + notes |

### Design settings (`PATCH /carousels/{id}/design`)

| Field | Type | Values | Default |
|-------|------|--------|---------|
| `template` | string | `bright` `classic` `comic` `elegant` `minimal` `notes` `powerful` | `classic` |
| `bg_color` | string | hex | template default |
| `bg_image_url` | string\|null | URL | `null` |
| `darkening` | float | 0.0–0.9 | `0.0` |
| `padding` | int | 0–200 | `40` |
| `align_h` | string | `left` `center` `right` | `center` |
| `align_v` | string | `top` `center` `bottom` | `center` |
| `aspect_ratio` | string | `4:5` `9:16` `1:1` | `4:5` |
| `accent_color` | string\|null | hex | template default |
| `title_highlight` | string\|null | hex | `null` |
| `pattern` | string | `none` `dots1` `dots2` `dots3` `grid` `lines` `cells` `blobs` | `none` |
| `pattern_color` | string | hex | `#000000` |
| `pattern_opacity` | float | 0.0–1.0 | `0.06` |
| `title_font` | string | `system` `playfair` `oswald` `montserrat` `opensans` `lato` `merriweather` `roboto_condensed` `jost` `fredoka` `caveat` `space_mono` | `system` |
| `body_font` | string | same as title_font | `system` |
| `show_header` | bool | | `false` |
| `header_text` | string | | `""` |
| `show_footer` | bool | | `false` |
| `footer_text` | string | | `""` |

### Slides

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/carousels/{id}/slides` | List all slides (ordered) |
| `PATCH` | `/carousels/{id}/slides/{slide_id}` | Update slide content or overrides |
| `PATCH` | `/carousels/{id}/slides/{slide_id}/order` | Reorder a slide `{new_order}` |
| `DELETE` | `/carousels/{id}/slides/{slide_id}` | Delete a slide |

**Update slide body** (all fields optional):
```json
{
  "title": "New Title",
  "body": "Updated body. Use ==highlighted== or **bold** inline.",
  "footer_cta": "Save this post",
  "overrides": {
    "bg_color": "#1a1a2e",
    "template": "elegant",
    "accent_color": "#d4af37"
  }
}
```

`overrides` accepts any design field and applies it to that slide only.

#### Inline markup

Two markers are supported in `title` and `body` fields:

| Syntax | Result |
|--------|--------|
| `==word==` | Highlight using the carousel accent color (white text) |
| `==#rrggbb\|#rrggbb\|word==` | Highlight with custom background and text color |
| `**word**` | Bold |

These render correctly in the live preview and in PNG exports.

### Generations

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/generations` | Start AI generation `{carousel_id}` |
| `GET` | `/generations/{id}` | Poll status |
| `GET` | `/generations/{id}/stream` | SSE stream for real-time status updates |

Status flow: `queued` → `running` → `done` | `failed`

### Exports

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/exports` | Start PNG export `{carousel_id}` |
| `GET` | `/exports/{id}` | Poll status + get download URL |
| `GET` | `/exports/{id}/stream` | SSE stream for real-time status updates |

Status flow: `queued` → `running` → `done` | `failed`

On `done`, `file_url` is a presigned MinIO URL (24h TTL) pointing to a ZIP of PNG slides.

| Aspect Ratio | Dimensions | Use case |
|-------------|------------|----------|
| `4:5` | 1080×1350 px | Instagram feed portrait |
| `9:16` | 1080×1920 px | Stories / Reels |
| `1:1` | 1080×1080 px | Square post |

### Assets

```
POST /assets/upload   multipart/form-data, field: "file"
```

Accepted types: `jpeg`, `png`, `webp`, `gif`. Max 10 MB.
Returns `{ "url": "..." }` — use as `bg_image_url` in design settings.

---

## Full Workflow (curl)

```bash
TOKEN="Bearer <your_jwt>"

# 1. Create carousel
curl -X POST http://localhost:8000/carousels \
  -H "Authorization: $TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"5 Python Tips","source_type":"text","source_payload":{"text":"Python is great..."},"format":{"slides_count":6,"language":"en"}}'
# → {"id": "abc-123", ...}

# 2. Generate slides
curl -X POST http://localhost:8000/generations \
  -H "Authorization: $TOKEN" -H "Content-Type: application/json" \
  -d '{"carousel_id": "abc-123"}'
# → {"id": "gen-456", "status": "queued"}

# 3. Poll until done
curl -H "Authorization: $TOKEN" http://localhost:8000/generations/gen-456
# → {"status": "done", "tokens_used": 712}

# 4. Export
curl -X POST http://localhost:8000/exports \
  -H "Authorization: $TOKEN" -H "Content-Type: application/json" \
  -d '{"carousel_id": "abc-123"}'

# 5. Download ZIP
curl -H "Authorization: $TOKEN" http://localhost:8000/exports/exp-789
# → {"status": "done", "file_url": "http://..."}
curl -L "<file_url>" -o slides.zip && unzip slides.zip
```

---

## Project Structure

```
generator/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py              # register, login, me, password, stats
│   │   │   ├── deps.py              # require_auth JWT dependency
│   │   │   └── routes/              # carousels, slides, generations, exports, assets
│   │   ├── core/                    # config, database, storage
│   │   ├── models/                  # User, Carousel, Slide, Generation, Export
│   │   ├── schemas/                 # Pydantic request/response models
│   │   └── services/
│   │       ├── llm.py               # AI generation (text/video/links source handling)
│   │       ├── export_svc.py        # Playwright HTML→PNG→ZIP pipeline
│   │       └── storage_svc.py       # MinIO upload/download
│   ├── alembic/versions/            # DB migrations
│   ├── fonts/                       # Bundled TTF fonts for export
│   └── requirements.txt
├── frontend/
│   ├── pages/
│   │   ├── index.vue                # Landing page
│   │   ├── login.vue / register.vue # Auth
│   │   ├── dashboard.vue            # Carousel list
│   │   ├── profile.vue              # Account settings
│   │   └── carousels/
│   │       ├── new.vue              # Creation wizard
│   │       └── [id]/edit.vue        # Visual editor
│   ├── components/
│   │   ├── SlidePreview.vue         # Live slide renderer (v-html + inline markup)
│   │   ├── CarouselCard.vue         # Dashboard card
│   │   └── DesignPanel.vue          # Design controls sidebar
│   ├── composables/                 # useAuth, useCarousels, useGeneration, useExport, useToast
│   ├── middleware/auth.global.ts    # JWT expiry check on every route
│   └── types/index.ts               # TypeScript interfaces + DEFAULT_DESIGN
├── docker-compose.yml
└── .env.example
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_API_KEY` | Yes | — | API key for your LLM provider |
| `JWT_SECRET` | Yes | random (resets on restart) | Secret for signing JWTs — set a stable value |
| `LLM_BASE_URL` | No | Groq endpoint | OpenAI-compatible chat completions URL |
| `LLM_MODEL` | No | `llama-3.3-70b-versatile` | Model name |
| `DATABASE_URL` | No | postgres in Docker | PostgreSQL asyncpg connection string |
| `MINIO_PUBLIC_URL` | No | `http://localhost:9000` | Public URL for presigned download links |
| `CORS_ORIGINS` | No | `*` | Comma-separated allowed origins |
| `JWT_EXPIRE_HOURS` | No | `72` | Token lifetime in hours |

> **Important:** If `JWT_SECRET` is not set, a random secret is generated per process start. All user sessions will be invalidated on every container restart.

---

## Known Limitations

| Area | Note |
|------|------|
| YouTube transcripts | Requires the video to have auto-generated or manual captions; private/age-restricted videos fall back to URL + notes |
| URL scraping | Some sites block scrapers or require JS — content fetch may fail silently and fall back to the raw URL |
| Export speed | Playwright launches a new Chromium process per export job; first export is slower while Chromium initialises |
| Rate limiting | The 30s generation cooldown is in-process; it resets on container restart |
| Concurrency | Generation and export run as FastAPI `BackgroundTasks` (in-process); use Celery + Redis for production scale |
| Export URL TTL | Presigned download URLs expire after 24 hours with no regeneration path |

---

## Local Development (without Docker)

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

export DATABASE_URL="postgresql+asyncpg://carousel:carousel@localhost:5432/carousel"
export LLM_API_KEY="gsk_..."
export JWT_SECRET="dev-secret"

alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
NUXT_PUBLIC_API_BASE=http://localhost:8000 npm run dev
```

---

## MinIO Console

**[http://localhost:9001](http://localhost:9001)** — username: `minioadmin` / password: `minioadmin`
