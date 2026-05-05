"""Tests for the data_schema module."""

from typing import Any

import pytest
from pydantic import ValidationError

from prismal.data_schema import (
    ExperimentDatasetBase,
    PromptDatasetBase,
    PromptRowBase,
    ResponseDatasetBase,
    ResponseRowBase,
)


def test_prompt_base_valid():
    """Test valid PromptRowBase initialization."""
    p = PromptRowBase(index=1, prompt="Hello")
    assert p.index == 1
    assert p.prompt == "Hello"


def test_prompt_base_invalid():
    """Test invalid PromptRowBase initialization."""
    invalid_index: Any = "not an int"
    with pytest.raises(ValidationError):
        PromptRowBase(index=invalid_index, prompt="Hello")


def test_prompt_schema_unique_index():
    """Test PromptDatasetBase unique index validation."""
    prompts = [
        PromptRowBase(index=1, prompt="P1"),
        PromptRowBase(index=2, prompt="P2"),
    ]
    PromptDatasetBase(prompts=prompts)

    invalid_prompts = [
        PromptRowBase(index=1, prompt="P1"),
        PromptRowBase(index=1, prompt="P2"),
    ]
    with pytest.raises(ValidationError, match="All indices must be unique"):
        PromptDatasetBase(prompts=invalid_prompts)


def test_response_base_valid():
    """Test valid ResponseRowBase initialization."""
    r = ResponseRowBase(index=1, responses=["R1", "R2"])
    assert r.index == 1
    assert r.responses == ["R1", "R2"]


def test_response_schema_valid():
    """Test valid ResponseDatasetBase initialization."""
    responses = [
        ResponseRowBase(index=1, responses=["A1", "B1"]),
        ResponseRowBase(index=2, responses=["A2", "B2"]),
    ]
    ResponseDatasetBase(responses=responses)


def test_response_schema_inconsistent_lengths():
    """Test ResponseDatasetBase inconsistent response lengths validation."""
    responses = [
        ResponseRowBase(index=1, responses=["A1", "B1"]),
        ResponseRowBase(index=2, responses=["A2"]),
    ]
    with pytest.raises(
        ValidationError, match="All cells must have the same number of responses"
    ):
        ResponseDatasetBase(responses=responses)


def test_response_schema_unique_index():
    """Test ResponseDatasetBase unique index validation."""
    responses = [
        ResponseRowBase(index=1, responses=["A1"]),
        ResponseRowBase(index=1, responses=["B1"]),
    ]
    with pytest.raises(ValidationError, match="All indices must be unique"):
        ResponseDatasetBase(responses=responses)


def test_response_schema_empty_responses():
    """Test ResponseDatasetBase with empty responses lists."""
    responses = [
        ResponseRowBase(index=1, responses=[]),
        ResponseRowBase(index=2, responses=[]),
    ]
    ResponseDatasetBase(responses=responses)


def test_dataset_schema_valid():
    """Test valid ExperimentDatasetBase initialization."""
    prompts = PromptDatasetBase(
        prompts=[
            PromptRowBase(index=1, prompt="P1"),
            PromptRowBase(index=2, prompt="P2"),
        ]
    )
    responses = ResponseDatasetBase(
        responses=[
            ResponseRowBase(index=1, responses=["R1"]),
            ResponseRowBase(index=2, responses=["R2"]),
        ]
    )
    ExperimentDatasetBase(prompts=prompts, responses=responses)


def test_dataset_schema_mismatch():
    """Test ExperimentDatasetBase with mismatched indices."""
    prompts = PromptDatasetBase(
        prompts=[
            PromptRowBase(index=1, prompt="P1"),
            PromptRowBase(index=2, prompt="P2"),
        ]
    )
    responses = ResponseDatasetBase(
        responses=[
            ResponseRowBase(index=1, responses=["R1"]),
            ResponseRowBase(index=3, responses=["R3"]),
        ]
    )
    with pytest.raises(
        ValidationError, match="Prompt and response indices must match exactly"
    ):
        ExperimentDatasetBase(prompts=prompts, responses=responses)
