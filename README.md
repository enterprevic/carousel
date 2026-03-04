# Carousel Generator MVP

An Instagram carousel generator. Create carousels from text or video, configure format, generate slides with AI (Claude), edit in a visual editor, and export as PNG ZIP.

## Stack

| Layer | Tech |
|-------|------|
| Backend | Python 3.12 + FastAPI + SQLAlchemy (async) + Alembic |
| Database | PostgreSQL 16 |
| Storage | MinIO (S3-compatible) |
| LLM | Any OpenAI-compatible API (default: Groq `llama-3.3-70b-versatile`) |
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

## API Examples

### Create a carousel
```bash
curl -X POST http://localhost:8000/carousels \
  -H "Content-Type: application/json" \
  -d '{
    "title": "5 Python Tips",
    "source_type": "text",
    "source_payload": {
      "text": "Python is great for automation. Use list comprehensions for cleaner code. F-strings are faster than format(). Type hints improve readability. Virtual environments keep dependencies clean."
    },
    "format": {
      "slides_count": 6,
      "language": "en",
      "style_hint": "Keep it punchy and actionable. Use emojis sparingly."
    }
  }'
```

### Trigger generation
```bash
curl -X POST http://localhost:8000/generations \
  -H "Content-Type: application/json" \
  -d '{"carousel_id": "<carousel-id-from-above>"}'
```

### Poll generation status
```bash
curl http://localhost:8000/generations/<generation-id>
# {"status": "queued|running|done|failed", "tokens_used": 1234, ...}
```

### Get slides
```bash
curl http://localhost:8000/carousels/<id>/slides
```

### Edit a slide
```bash
curl -X PATCH http://localhost:8000/carousels/<id>/slides/<slide-id> \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title", "body": "Updated body text"}'
```

### Update design
```bash
curl -X PATCH http://localhost:8000/carousels/<id>/design \
  -H "Content-Type: application/json" \
  -d '{
    "template": "bold",
    "bg_color": "#1a1a1a",
    "padding": 50,
    "align_h": "left",
    "align_v": "center",
    "show_footer": true,
    "footer_text": "Follow for more"
  }'
```

### Export to ZIP
```bash
# Start export
curl -X POST http://localhost:8000/exports \
  -H "Content-Type: application/json" \
  -d '{"carousel_id": "<id>"}'

# Poll status
curl http://localhost:8000/exports/<export-id>
# {"status": "done", "file_url": "http://localhost:9000/carousel-assets/exports/.../xxx.zip"}

# Download
curl -L "<file_url>" -o slides.zip
unzip slides.zip
# → slide_01.png, slide_02.png, ...
```

### Upload background image
```bash
curl -X POST http://localhost:8000/assets/upload \
  -F "file=@/path/to/image.jpg"
# → {"url": "http://localhost:9000/carousel-assets/assets/...jpg"}
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
│   ├── components/          # CarouselCard, SlidePreview, DesignPanel
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
- Slide generation via Claude `claude-sonnet-4-6` with JSON validation + 1 retry
- Export: Playwright renders each slide as HTML → screenshot → PNG → ZIP → MinIO
- Slide size: **1080×1350px** (Instagram 4:5 ratio)
- MinIO for asset storage with public read policy

### Frontend
- Nuxt 3 + Vue 3 Composition API + Pinia
- Desktop + mobile responsive layout
- Creation wizard (3 steps: source type → content → format)
- Visual editor with slide thumbnails, text editing, and design panel
- Design panel tabs: Template / Background / Layout / Header+Footer
- 3 slide templates: Classic / Bold / Minimal
- Auto-save on blur for slide text
- Export button with polling and download link

---

## Known Limitations & Simplifications

| Area | Limitation |
|------|-----------|
| **Video** | Accepts URL only; no actual video transcription (LLM uses URL + notes as context) |
| **Export speed** | First export is slow (~30-60s) because Playwright launches Chromium. Subsequent exports are faster. |
| **Fonts** | Export uses system fonts (Noto CJK included in Docker image for CJK characters) |
| **Auth** | No authentication in MVP. API is open. |
| **Generation polling** | Frontend polls every 2s via REST. No WebSockets/SSE. |
| **Preview images** | Carousel list shows CSS-rendered preview (not actual PNG screenshots). |
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
export ANTHROPIC_API_KEY="sk-ant-..."
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

---

## Slide Export Format

- Size: 1080×1350 px (Instagram 4:5 portrait)
- Format: PNG (lossless)
- Naming: `slide_01.png`, `slide_02.png`, …
- Delivery: ZIP archive via presigned MinIO URL (1-hour TTL)
