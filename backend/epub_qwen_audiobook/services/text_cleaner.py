from bs4 import BeautifulSoup
import re
from typing import List
from ..models.book import TextChunk, Chapter


class TextCleaner:
    """
    Cleans HTML content and splits text into manageable chunks for TTS.
    """

    def __init__(self, min_chunk_size: int = 300, max_chunk_size: int = 800):
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size

    def clean_html(self, html_content: str) -> str:
        """
        Strips HTML and handles Japanese rubies specifically.
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Handle Rubies: Keep only the base text (the text inside <ruby> but NOT inside <rt>)
        for ruby in soup.find_all("ruby"):
            # Extract all text nodes that are direct children of <ruby> and NOT inside <rt>
            base_text = "".join(
                [
                    t
                    for t in ruby.contents
                    if isinstance(t, str) or (hasattr(t, "name") and t.name != "rt")
                ]
            )
            # Replace the ruby tag with just the base text
            ruby.replace_with(base_text)

        # Get plain text
        text = soup.get_text(separator=" ")

        # Clean up whitespace and special characters
        text = re.sub(r"\s+", " ", text)  # Normalize spaces
        text = text.strip()

        return text

    def split_into_chunks(self, text: str) -> List[TextChunk]:
        """
        Splits text into chunks based on size and natural boundaries (periods, etc.).
        """
        chunks = []
        start = 0
        chunk_index = 1

        while start < len(text):
            end = start + self.max_chunk_size
            if end >= len(text):
                end = len(text)
            else:
                # Try to find a natural break (., !, ?, \n) near the end of the chunk
                break_point = -1
                for char in [".", "！", "？", "。", "\n"]:
                    pos = text.rfind(char, start + self.min_chunk_size, end)
                    if pos > break_point:
                        break_point = pos

                if break_point != -1:
                    end = break_point + 1
                else:
                    # No natural break, just cut at max_chunk_size
                    end = self.max_chunk_size + start

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(TextChunk(index=chunk_index, text=chunk_text))
                chunk_index += 1

            start = end

        return chunks

    def process_chapter(self, chapter: Chapter) -> Chapter:
        """
        Full pipeline: HTML -> Clean Text -> Chunks.
        """
        clean_text = self.clean_html(chapter.content)
        chapter.chunks = self.split_into_chunks(clean_text)
        return chapter
