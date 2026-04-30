from pydub import AudioSegment
from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)


class AudioMerger:
    """
    Combines multiple audio chunks into a single audio file.
    """

    @staticmethod
    def merge_chunks(
        chunk_paths: List[Path], output_path: Path, format: str = "mp3"
    ) -> bool:
        """
        Merges a list of WAV/MP3 chunks into one output file.
        """
        if not chunk_paths:
            logger.warning("No chunks provided for merging.")
            return False

        try:
            combined = AudioSegment.empty()
            for path in chunk_paths:
                if path.exists():
                    audio = AudioSegment.from_file(str(path))
                    combined += audio
                else:
                    logger.warning(f"Chunk file missing: {path}")

            combined.export(str(output_path), format=format)
            return True

        except Exception as e:
            logger.error(f"Error merging audio chunks: {e}")
            return False
