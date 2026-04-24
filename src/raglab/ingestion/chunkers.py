def recursive_chunk(
    text: str,
    chunk_size: int = 512,
    overlap: int = 50,
) -> list[str]:
    """
    Split text into overlapping chunks of approximately chunk_size characters.

    Args:
        text: raw text to split
        chunk_size: maximum characters per chunk
        overlap: number of characters to repeat between consecutive chunks

    Returns:
        list of text chunks
    """
    raise NotImplementedError