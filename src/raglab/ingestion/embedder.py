from raglab.config import settings


def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Convert a list of strings into embedding vectors using OpenAI.

    Args:
        texts: list of text chunks to embed

    Returns:
        list of vectors, one per input text
    """
    raise NotImplementedError