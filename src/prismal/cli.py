"""CLI utilities for prismal."""

import argparse


def add_common_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Add common arguments to an argument parser.

    The following arguments are added:
    - -c, --config: Path to the configuration file (required).
    - -i, --input: Path to the input data file (optional, overrides config).
    - -o, --output: Path to the output results file (optional, overrides config).
    - -m, --model: Model ID to use (optional, overrides config).

    Args:
        parser: The argument parser to add arguments to.

    Returns:
        The argument parser with common arguments added.
    """
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=True,
        help="Path to the configuration file.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="input data path relative to repo root(overrides config).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output path, relative to repo root (overrides config).",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="Model ID to use (overrides config).",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        help="Temperature for sampling (overrides config).",
    )
    parser.add_argument(
        "--max-concurrency",
        type=int,
        help="Maximum number of concurrent requests (overrides config).",
    )
    parser.add_argument(
        "--rpm-limit",
        type=int,
        help="Maximum requests per minute (overrides config).",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        help="Maximum number of retries per request (overrides config).",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO).",
    )
    return parser
