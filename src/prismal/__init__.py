"""Prismal: template for AI/ML research."""

from prismal.data_schema import (
    ExperimentDatasetBase,
    PromptDatasetBase,
    PromptRowBase,
    ResponsesDatasetBase,
    ResponsesRowBase,
)


def hello() -> str:
    """hello-world to confirm installation."""
    return "Hello from prismal!"


__all__ = [
    "ExperimentDatasetBase",
    "PromptDatasetBase",
    "PromptRowBase",
    "ResponsesDatasetBase",
    "ResponsesRowBase",
]
