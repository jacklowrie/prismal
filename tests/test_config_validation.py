from pathlib import Path

import pytest
from pydantic import ValidationError

from prismal.config import (
    ComputeConfig,
    ConfigBase,
    DataConfig,
    ExperimentConfig,
    ModelConfig,
)


def test_config_model_requires_model_or_path():
    """Test that ConfigBase requires either model.id or model.path."""
    experiment = ExperimentConfig(name="test", task="test")
    data = DataConfig(input=Path("data/input.csv"), output=Path("outputs"))
    compute = ComputeConfig(location="remote", url="http://api.example.com")

    # We want it to fail if both are missing
    with pytest.raises(ValidationError):
        ConfigBase(
            experiment=experiment,
            data=data,
            compute=compute,
            model=ModelConfig(num_samples=100, seed=42),  # type: ignore[call-arg]
        )

    # We want it to fail if both are present
    with pytest.raises(ValidationError):
        ConfigBase(
            experiment=experiment,
            data=data,
            compute=compute,
            model=ModelConfig(
                id="gpt-4", path=Path("model_id.txt"), num_samples=100, seed=42
            ),
        )

    # We want it to pass with only model.id
    config_model = ConfigBase(
        experiment=experiment,
        data=data,
        compute=compute,
        model=ModelConfig(id="gpt-4", num_samples=100, seed=42),
    )
    assert config_model.model.id == "gpt-4"

    # We want it to pass with only model.path
    config_path = ConfigBase(
        experiment=experiment,
        data=data,
        compute=compute,
        model=ModelConfig(path=Path("model_id.txt"), num_samples=100, seed=42),
    )
    assert config_path.model.path == Path("model_id.txt")
