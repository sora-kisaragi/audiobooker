from backend.epub_qwen_audiobook.services.text_cleaner import TextCleaner


def test_text_cleaner_ruby_removal():
    cleaner = TextCleaner()
    html = "<p>これは<ruby>漢字<rt>かんじ</rt></ruby>です</p>"
    # Should keep "漢字" and remove "かんじ"
    result = cleaner.clean_html(html)
    assert "漢字" in result
    assert "かんじ" not in result


def test_text_cleaner_chunking():
    cleaner = TextCleaner(min_chunk_size=10, max_chunk_size=20)
    text = "This is a long piece of text that should be split into several smaller chunks for testing purposes."
    chunks = cleaner.split_into_chunks(text)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk.text) <= 20
