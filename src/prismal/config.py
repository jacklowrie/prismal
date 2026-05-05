"""Configuration schema/loading and common paths for prismal."""

from pathlib import Path
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, PositiveInt, model_validator

if TYPE_CHECKING:
    pass


class ConfigBase(BaseModel):
    """Base configuration model for Prismal.

    This model defines the common configuration parameters used across the
    Prismal project.

    Attributes:
        num_samples: Number of samples to process in the experiment.
        inference_location: Location or service where inference is performed.
            Must be either "local" or "remote".
        inference_url: URL for remote inference. Required if inference_location
            is "remote".
        input: Path to the input data file.
        output: Path where the experiment results will be saved.
        model_id: ID/slug of the model to use.
        models_path: Path to a file containing the model id's, one per line.
    """

    num_samples: PositiveInt
    inference_location: Literal["local", "remote"]
    inference_url: str | None = None
    input: Path
    output: Path
    model_id: str | None = None
    models_path: Path | None = None

    @model_validator(mode="after")
    def validate_inference_config(self) -> "ConfigBase":
        """Validate inference configuration.

        Ensures that:
        1. Either model_id or models_path is provided, but not both.
        2. inference_url is provided if inference_location is "remote".
        """
        if (self.model_id is not None) == (self.models_path is not None):
            msg = "Exactly one of 'model_id' or 'models_path' must be provided."
            raise ValueError(msg)

        if self.inference_location == "remote" and not self.inference_url:
            msg = "inference_url must be provided when inference_location is 'remote'."
            raise ValueError(msg)

        return self

    def get_model_ids(self) -> list[str]:
        """Get the list of model IDs to use.

        If model_id is set, returns a list with that single ID.
        If models_path is set, reads the IDs from that file.

        Returns:
            A list of model ID strings.
        """
        if self.model_id:
            return [self.model_id]

        if self.models_path:
            from prismal.io import read_model_ids

            return read_model_ids(self.models_path)

        # This should be unreachable due to the model_validator
        return []


def _find_root() -> Path:
    """Find the root directory of the project.

    This searches upwards from the current file for a 'pyproject.toml' file.
    """
    path = Path(__file__).resolve()
    for parent in path.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    # Fallback if no pyproject.toml is found
    return path.parent.parent.parent


# Root directory of the project.
ROOT_DIR: Path = _find_root()

# Directory for configuration files.
CONFIG_DIR: Path = ROOT_DIR / "config"

# Directory for raw and processed data.
DATA_DIR: Path = ROOT_DIR / "data"

# Directory for experiment outputs and results.
OUTPUT_DIR: Path = ROOT_DIR / "outputs"
