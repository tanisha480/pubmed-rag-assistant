def chunk_text(text: str, max_chars: int = 2000):
    """Split text into chunks of at most max_chars, breaking at line boundaries."""
    lines = text.split("\n")
    chunks = []
    current = ""

    for line in lines:
        if len(current) + len(line) + 1 > max_chars:
            if current.strip():
                chunks.append(current.strip())
            current = ""
        current += line + "\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks
