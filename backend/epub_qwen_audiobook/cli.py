import typer
import asyncio
from pathlib import Path
from .services.epub_loader import EpubLoader
from .services.text_cleaner import TextCleaner
from .services.tts_client import QwenTTSClient
from .services.audio_merger import AudioMerger

app = typer.Typer()


async def run_conversion(
    epub_path: Path, output_dir: Path, tts_url: str, profile: str, language: str
):
    # 1. Load EPUB
    loader = EpubLoader(str(epub_path))
    metadata = loader.extract_metadata()
    chapters = loader.extract_chapters()

    print(f"📖 Processing: {metadata.title} by {metadata.author}")
    print(f"🌐 TTS Server: {tts_url} (Profile: {profile})")

    # 2. Clean and Chunk
    cleaner = TextCleaner()
    for chapter in chapters:
        chapter = cleaner.process_chapter(chapter)

    # 3. Synthesis
    tts_client = QwenTTSClient(tts_url, profile, language)

    # Ensure output directories exist
    chapters_audio_dir = output_dir / "chapters"
    chunks_audio_dir = output_dir / "chunks"
    chapters_audio_dir.mkdir(parents=True, exist_ok=True)
    chunks_audio_dir.mkdir(parents=True, exist_ok=True)

    for chapter in chapters:
        print(f"🎙️ Synthesizing Chapter {chapter.index}: {chapter.title}...")
        chunk_files = []

        for chunk in chapter.chunks:
            chunk_filename = f"ch{chapter.index}_chunk{chunk.index}.wav"
            chunk_path = chunks_audio_dir / chunk_filename

            success = await tts_client.synthesize(chunk.text, chunk_path)
            if success:
                chunk.audio_file = str(chunk_path)
                chunk_files.append(chunk_path)
            else:
                print(f"  ❌ Failed to synthesize chunk {chunk.index}")

        # 4. Merge
        chapter_filename = f"{chapter.index:03d}_{chapter.title.replace(' ', '_')}.mp3"
        chapter_path = chapters_audio_dir / chapter_filename

        if chunk_files:
            if AudioMerger.merge_chunks(chunk_files, chapter_path):
                print(f"  ✅ Saved: {chapter_filename}")
            else:
                print(f"  ❌ Failed to merge audio for chapter {chapter.index}")
        else:
            print(f"  ⚠️ No audio generated for chapter {chapter.index}")

    print("\n✨ Conversion Complete!")
    print(f"Files saved to: {output_dir}")


@app.command()
def convert(
    epub: Path = typer.Option(..., "--epub", help="Path to the input EPUB file"),
    output: Path = typer.Option(..., "--output", help="Output directory"),
    tts_url: str = typer.Option(
        "http://localhost:8087", "--tts-url", help="Qwen-TTS API server URL"
    ),
    profile: str = typer.Option("default.pt", "--profile", help="TTS voice profile"),
    language: str = typer.Option("japanese", "--language", help="Target language"),
):
    """
    Convert an EPUB file to an audiobook.
    """
    asyncio.run(run_conversion(epub, output, tts_url, profile, language))


if __name__ == "__main__":
    app()
