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
    config = ConfigBase(
        num_samples=100,
        inference_location="remote",
        inference_url="http://api.example.com",
        input=Path("data/input.csv"),
        output=Path("outputs/results.json"),
        model_id="gpt-4",
    )
    assert config.num_samples == 100
    assert config.inference_location == "remote"
    assert config.inference_url == "http://api.example.com"
    assert config.input.name == "input.csv"
    assert config.output.name == "results.json"
    assert config.model_id == "gpt-4"
    assert config.get_model_ids() == ["gpt-4"]


def test_config_get_model_ids_from_path(tmp_path: Path) -> None:
    """Test get_model_ids when models_path is provided."""
    models_file = tmp_path / "models.txt"
    models_file.write_text("gpt-4\nclaude-3-opus", encoding="utf-8")

    config = ConfigBase(
        num_samples=10,
        inference_location="local",
        input=Path("in.csv"),
        output=Path("out.json"),
        models_path=models_file,
    )
    assert config.get_model_ids() == ["gpt-4", "claude-3-opus"]
