"""Configuration and common paths for prismal."""

from pathlib import Path

from pydantic import BaseModel, PositiveInt


class ConfigBase(BaseModel):
    """Base Configuration model for prismal.

    Attributes:
        num_samples: Number of samples to process.
        inference_location: Location where inference is performed.
        input: Path to the input file.
        output: Path to the output file.
    """

    num_samples: PositiveInt
    inference_location: str
    input: Path
    output: Path


# Root of the project
ROOT_DIR: Path = Path(__file__).parent.parent.parent.resolve()

# Config directory
CONFIG_DIR: Path = ROOT_DIR / "config"

# Data directory
DATA_DIR: Path = ROOT_DIR / "data"

# Output directory
OUTPUT_DIR: Path = ROOT_DIR / "outputs"
