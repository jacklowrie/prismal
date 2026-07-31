"""Configuration schema/loading and common paths for prismal."""

import tomllib
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Self

from pydantic import BaseModel, PositiveInt, model_validator

if TYPE_CHECKING:
    pass


class ExperimentConfig(BaseModel):
    """Experiment configuration.

    Attributes:
        name: Name of the experiment.
        task: Task being performed in the experiment.
    """

    name: str
    task: str


class DataConfig(BaseModel):
    """Data configuration.

    Attributes:
        input: Path to the input data file.
        output: Path to the base directory where experiment results will be saved.
    """

    input: Path
    output: Path


class ComputeConfig(BaseModel):
    """Compute configuration.

    Attributes:
        location: Location or service where inference is performed.
            Must be either "local" or "remote".
        url: URL for remote inference. Required if location is "remote".
        max_concurrency: Maximum number of concurrent requests.
    """

    location: Literal["local", "remote"]
    url: str | None = None
    max_concurrency: PositiveInt = 10
    requests_per_minute: PositiveInt = 20
    max_retries: PositiveInt = 5

    @model_validator(mode="after")
    def validate_compute_config(self) -> Self:
        """Validate compute configuration.

        Ensures that url is provided if location is "remote".
        """
        if self.location == "remote" and not self.url:
            msg = "url must be provided when location is 'remote'."
            raise ValueError(msg)

        return self


class ModelConfig(BaseModel):
    """Model configuration.

    Attributes:
        id: ID/slug of the model to use.
        path: Path to a file containing the model IDs, one per line.
        num_samples: Number of samples to process in the experiment.
        temperature: Temperature for sampling.
        seed: Random seed for reproducibility.
    """

    id: str | None = None
    path: Path | None = None  # Relative paths resolved against CONFIG_DIR
    num_samples: PositiveInt
    temperature: float = 0.7
    seed: int

    @model_validator(mode="after")
    def validate_model_config(self) -> Self:
        """Validate model configuration.

        Ensures that exactly one of 'id' or 'path' is provided.
        """
        if (self.id is not None) == (self.path is not None):
            msg = "Exactly one of 'id' or 'path' must be provided."
            raise ValueError(msg)

        return self


class ConfigBase(BaseModel):
    """Base configuration model for Prismal.

    This model defines the common configuration parameters used across the
    Prismal project, organized into sections.

    Attributes:
        experiment: Experiment configuration section.
        data: Data configuration section.
        compute: Compute configuration section.
        model: Model configuration section.
    """

    experiment: ExperimentConfig
    data: DataConfig
    compute: ComputeConfig
    model: ModelConfig

    @property
    def output_dir(self) -> Path:
        """Get the experiment-specific output directory.

        The directory is constructed as `data.output / experiment.name`.
        If the path is relative, it is resolved against `ROOT_DIR`.

        Returns:
            The path to the experiment output directory.
        """
        path = self.data.output / self.experiment.name
        if not path.is_absolute():
            path = ROOT_DIR / path
        return path

    @classmethod
    def from_toml(cls, path: Path | str) -> Self:
        """Load configuration from a TOML file.

        Args:
            path: Path to the TOML configuration file.

        Returns:
            An instance of ConfigBase populated from the TOML file.
        """
        with Path(path).open("rb") as f:
            data = tomllib.load(f)
        return cls(**data)

    def get_model_ids(self) -> list[str]:
        """Get the list of model IDs to use.

        If id is set, returns a list with that single ID.
        If path is set, reads the IDs from that file. Relative paths are
        resolved against CONFIG_DIR.

        Returns:
            A list of model ID strings.
        """
        if self.model.id:
            return [self.model.id]

        if self.model.path:
            path = self.model.path
            if not path.is_absolute():
                path = CONFIG_DIR / path

            from prismal.io import read_model_ids

            return read_model_ids(path)

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
CONFIG_DIR: Path = ROOT_DIR / "configs"

# Directory for raw and processed data.
DATA_DIR: Path = ROOT_DIR / "data"

# Directory for experiment outputs and results.
OUTPUT_DIR: Path = ROOT_DIR / "outputs"
