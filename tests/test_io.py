"""Tests for the io module."""

from pathlib import Path

import pytest

from prismal.io import read_model_ids


def test_read_model_ids(tmp_path: Path) -> None:
    """Test reading model IDs from a file."""
    p = tmp_path / "models.txt"
    p.write_text("gpt-4\nclaude-3-opus\n\n  llama-3  \n", encoding="utf-8")

    model_ids = read_model_ids(p)
    assert model_ids == ["gpt-4", "claude-3-opus", "llama-3"]


def test_read_model_ids_not_found() -> None:
    """Test that it raises FileNotFoundError if the file doesn't exist."""
    with pytest.raises(FileNotFoundError, match="Model IDs file not found"):
        read_model_ids(Path("non_existent_file.txt"))
