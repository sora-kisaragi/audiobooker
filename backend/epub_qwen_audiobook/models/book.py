from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TextChunk:
    index: int
    text: str
    audio_file: Optional[str] = None
    duration_sec: Optional[float] = None
    start_sec: Optional[float] = None
    end_sec: Optional[float] = None


@dataclass
class Chapter:
    index: int
    title: str
    content: str
    chunks: List[TextChunk] = field(default_factory=list)
    audio_file: Optional[str] = None
    duration_sec: Optional[float] = None


@dataclass
class BookMetadata:
    title: str
    author: str
    language: str
    cover_image_path: Optional[str] = None
