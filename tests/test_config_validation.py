from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from prismal.config import ConfigBase


def test_config_model_requires_model_or_path():
    """Test that ConfigBase requires either model_id or models_path."""
    common: dict[str, Any] = {
        "num_samples": 100,
        "inference_location": "remote",
        "inference_url": "http://api.example.com",
        "input": Path("data/input.csv"),
        "output": Path("outputs/results.json"),
    }

    # We want it to fail if both are missing
    with pytest.raises(ValidationError):
        ConfigBase(**common)  # type: ignore[arg-type]

    # We want it to fail if both are present
    with pytest.raises(ValidationError):
        ConfigBase(**common, model_id="gpt-4", models_path=Path("model_id.txt"))  # type: ignore[arg-type]

    # We want it to pass with only model_id
    config_model = ConfigBase(**common, model_id="gpt-4")  # type: ignore[arg-type]
    assert config_model.model_id == "gpt-4"

    # We want it to pass with only models_path
    config_path = ConfigBase(**common, models_path=Path("model_id.txt"))  # type: ignore[arg-type]
    assert config_path.models_path == Path("model_id.txt")
