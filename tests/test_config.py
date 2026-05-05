"""Tests for the config module."""

from pathlib import Path

from prismal.config import DATA_DIR, OUTPUT_DIR, ROOT_DIR, ConfigBase


def test_paths() -> None:
    """Test that the paths are correctly resolved."""
    # Check that ROOT_DIR is the root of the project (contains pyproject.toml)
    assert (ROOT_DIR / "pyproject.toml").exists()
    assert ROOT_DIR.is_absolute()

    # Check that DATA_DIR and OUTPUT_DIR are subdirectories of ROOT_DIR
    assert DATA_DIR == ROOT_DIR / "data"
    assert OUTPUT_DIR == ROOT_DIR / "outputs"

    # We don't necessarily check if they exist because they might not be created yet,
    # but based on guidelines they should exist in the project structure for
    # scripts to use.


def test_config_model() -> None:
    """Test that ConfigBase works as expected."""
    data = {
        "num_samples": 100,
        "inference_location": "remote",
        "input": Path("data/input.csv"),
        "output": Path("outputs/results.json"),
    }
    config = ConfigBase(**data)
    assert config.num_samples == 100
    assert config.inference_location == "remote"
    assert config.input.name == "input.csv"
    assert config.output.name == "results.json"
