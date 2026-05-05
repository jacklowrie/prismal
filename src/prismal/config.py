"""Configuration schema/loading and common paths for prismal."""

from pathlib import Path
from typing import TYPE_CHECKING

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
        input: Path to the input data file.
        output: Path where the experiment results will be saved.
        model_id: ID/slug of the model to use.
        models_path: Path to a file containing the model id's, one per line.
    """

    num_samples: PositiveInt
    inference_location: str
    input: Path
    output: Path
    model_id: str | None = None
    models_path: Path | None = None

    @model_validator(mode="after")
    def check_model_or_path(self) -> "ConfigBase":
        """Ensure that either model_id or models_path is provided, but not both."""
        if (self.model_id is not None) == (self.models_path is not None):
            msg = "Exactly one of 'model_id' or 'models_path' must be provided."
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


# Root directory of the project.
ROOT_DIR: Path = Path(__file__).parent.parent.parent.resolve()

# Directory for configuration files.
CONFIG_DIR: Path = ROOT_DIR / "config"

# Directory for raw and processed data.
DATA_DIR: Path = ROOT_DIR / "data"

# Directory for experiment outputs and results.
OUTPUT_DIR: Path = ROOT_DIR / "outputs"
