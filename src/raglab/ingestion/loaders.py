# two functions:
# load_pdf(path: str) -> list[dict]
# load_markdown(path: str) -> list[dict]
# each returns list of {"text": str, "source": str, "page": int}

from pathlib import Path

def load_pdf(path: str) -> list[dict]:
    """
    Extract text from a PDF file page by page.
    
    Args:
        path: absolute or relative path to the PDF file
        
    Returns: 
        list of dicts with keys: text, source, page
    """

    raise NotImplementedError

def load_markdown(path: str) -> list[dict]:
    """
    Load a Markdown file as a single document.
    
    Args: 
        path: absolute or relative path to the .md file
        
    Returns:
        list with a single dict with keys: text, source, page
    """

    raise NotImplementedError