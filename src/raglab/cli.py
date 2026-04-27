from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def ingest(corpus_path: Path) -> None:
    """
    Ingest all PDF and Markdown files from a directory into ChromaDB.

    Args:
        corpus_path: path to directory containing documents
    """
    raise NotImplementedError


if __name__ == "__main__":
    app()
