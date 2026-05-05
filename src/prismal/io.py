"""I/O utilities for prismal."""

from pathlib import Path


def read_model_ids(path: Path) -> list[str]:
    """Read model IDs from a file, one per line.

    Args:
        path: Path to the file containing model IDs.

    Returns:
        A list of model IDs, with whitespace stripped and empty lines ignored.
    """
    if not path.exists():
        msg = f"Model IDs file not found: {path}"
        raise FileNotFoundError(msg)

    with path.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
