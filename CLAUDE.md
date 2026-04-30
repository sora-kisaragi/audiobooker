# EPUB Audiobook Generator (Qwen-TTS)

This project converts EPUB files into audiobooks using the Qwen-TTS API server, providing a manifest-based structure for a playback UI.

## Project Goals
- Convert EPUB to chapter-based audio files.
- Generate a `manifest.json` for synchronization and playback.
- Provide a Web UI for library management and audio playback.

## Tech Stack
- **Backend/CLI**: Python, Typer, ebooklib, BeautifulSoup4, httpx, pydub/ffmpeg.
- **Frontend**: React, TypeScript, Tailwind CSS, Zustand, FastAPI.
- **TTS Engine**: Qwen-TTS API (`/tts/voice-clone/profile`).

## Development Guidelines
- **Code Style**: Python (PEP 8), TypeScript (Strict).
- **Architecture**: Layered architecture (Services -> Core -> API).
- **Error Handling**: Validate all external API calls; use a manifest to allow resumable conversions.
- **Documentation**: Keep `CLAUDE.md` updated with key architectural decisions.

## Build & Test Commands
- CLI: `python -m epub_qwen_audiobook convert ...`
- Backend: `uvicorn backend.app.main:app --reload`
- Frontend: `npm run dev`
- Tests: `pytest`
