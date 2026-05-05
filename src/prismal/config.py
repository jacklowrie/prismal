"""Configuration schema/loading and common paths for prismal."""

from pathlib import Path

from pydantic import BaseModel, PositiveInt, model_validator


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
        models_path: Path to a file containing the model name.
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


# Root directory of the project.
ROOT_DIR: Path = Path(__file__).parent.parent.parent.resolve()

# Directory for configuration files.
CONFIG_DIR: Path = ROOT_DIR / "config"

# Directory for raw and processed data.
DATA_DIR: Path = ROOT_DIR / "data"

# Directory for experiment outputs and results.
OUTPUT_DIR: Path = ROOT_DIR / "outputs"
