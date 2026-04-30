import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from typing import List
from ..models.book import BookMetadata, Chapter


class EpubLoader:
    """
    Handles loading and initial extraction of EPUB files.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.book = epub.read_epub(file_path)

    def extract_metadata(self) -> BookMetadata:
        """
        Extracts basic metadata from the EPUB.
        """
        title = (
            self.book.get_metadata("DC", "title")[0][0]
            if self.book.get_metadata("DC", "title")
            else "Unknown Title"
        )
        author = (
            self.book.get_metadata("DC", "creator")[0][0]
            if self.book.get_metadata("DC", "creator")
            else "Unknown Author"
        )
        language = (
            self.book.get_metadata("DC", "language")[0][0]
            if self.book.get_metadata("DC", "language")
            else "ja"
        )

        # Try to find cover image
        cover_image_path = None
        # Simplified cover extraction: in a real app, we'd save the image to disk
        # For now, we just note it exists if found
        if self.book.get_item_with_id("cover"):
            cover_image_path = "cover.jpg"  # Placeholder

        return BookMetadata(
            title=title,
            author=author,
            language=language,
            cover_image_path=cover_image_path,
        )

    def extract_chapters(self) -> List[Chapter]:
        """
        Extracts chapters from the EPUB.
        Filters for documents that are likely to be chapters.
        """
        chapters = []
        chapter_index = 1

        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Basic heuristic: if it's a document and has content, treat as chapter
                # In a real app, we'd use the TOC (Table of Contents)
                soup = BeautifulSoup(item.get_content(), "html.parser")

                # Attempt to find a chapter title from h1, h2 or the title attribute
                title = soup.find(["h1", "h2", "h3"])
                chapter_title = (
                    title.get_text().strip() if title else f"Chapter {chapter_index}"
                )

                chapters.append(
                    Chapter(
                        index=chapter_index,
                        title=chapter_title,
                        content=str(soup),  # Pass raw HTML for the cleaner
                    )
                )
                chapter_index += 1

        return chapters
