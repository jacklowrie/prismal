"""Tests for the config module."""

from pathlib import Path

from prismal.config import (
    DATA_DIR,
    OUTPUT_DIR,
    ROOT_DIR,
    ComputeConfig,
    ConfigBase,
    DataConfig,
    ExperimentConfig,
    ModelConfig,
)


def test_paths() -> None:
    """Test that the paths are correctly resolved."""
    # Check that ROOT_DIR is the root of the project (contains pyproject.toml)
    assert (ROOT_DIR / "pyproject.toml").exists()
    assert ROOT_DIR.is_absolute()

    # Check that DATA_DIR and OUTPUT_DIR are subdirectories of ROOT_DIR
    assert DATA_DIR == ROOT_DIR / "data"
    assert OUTPUT_DIR == ROOT_DIR / "outputs"


def test_config_model() -> None:
    """Test that ConfigBase works as expected."""
    config = ConfigBase(
        experiment=ExperimentConfig(name="test-exp", task="test-task"),
        data=DataConfig(input=Path("data/input.csv"), output=Path("outputs")),
        compute=ComputeConfig(location="remote", url="http://api.example.com"),
        model=ModelConfig(id="gpt-4", num_samples=100, seed=42),
    )
    assert config.model.num_samples == 100
    assert config.compute.location == "remote"
    assert config.compute.url == "http://api.example.com"
    assert config.data.input.name == "input.csv"
    assert config.output_dir.name == "test-exp"
    assert config.model.id == "gpt-4"
    assert config.get_model_ids() == ["gpt-4"]


def test_config_get_model_ids_from_path(tmp_path: Path) -> None:
    """Test get_model_ids when model.path is provided."""
    models_file = tmp_path / "models.txt"
    models_file.write_text("gpt-4\nclaude-3-opus", encoding="utf-8")

    config = ConfigBase(
        experiment=ExperimentConfig(name="test-exp", task="test-task"),
        data=DataConfig(input=Path("in.csv"), output=Path("out")),
        compute=ComputeConfig(location="local"),
        model=ModelConfig(path=models_file, num_samples=10, seed=42),
    )
    assert config.get_model_ids() == ["gpt-4", "claude-3-opus"]
