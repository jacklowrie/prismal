"""Data schema definitions for prismal."""

from pydantic import BaseModel, Field, model_validator


class PromptRowBase(BaseModel):
    """Base model for prompts.

    Attributes:
        index: A unique dataset-level identifier for the prompt.
        prompt: The prompt string.
    """

    index: int = Field(..., description="A unique identifier for the prompt.")
    prompt: str = Field(..., description="The prompt string.")


class ResponsesRowBase(BaseModel):
    """Base model for responses.

    Attributes:
        index: A unique identifier for the response, corresponding to a prompt index.
        responses: A list of response strings.
        response: The first response string, or an empty string if no responses exist.
    """

    index: int = Field(..., description="A unique identifier for the response.")
    responses: list[str] = Field(..., description="A list of response strings.")

    @property
    def response(self) -> str:
        """The first response string, or an empty string if no responses exist."""
        return self.responses[0] if self.responses else ""


class PromptDatasetBase(BaseModel):
    """Schema for a collection of prompts.

    Attributes:
        prompts: A list of PromptRowBase objects.
    """

    prompts: list[PromptRowBase]

    @model_validator(mode="after")
    def check_unique_index(self) -> "PromptDatasetBase":
        """Check that all indices are unique."""
        indices = [p.index for p in self.prompts]
        if len(indices) != len(set(indices)):
            msg = "All indices must be unique."
            raise ValueError(msg)
        return self


class ResponsesDatasetBase(BaseModel):
    """Schema for a collection of responses.

    Attributes:
        responses: A list of ResponsesRowBase objects.
    """

    responses: list[ResponsesRowBase]

    @model_validator(mode="after")
    def check_schema_consistency(self) -> "ResponsesDatasetBase":
        """Check for unique indices and consistent response lengths."""
        if not self.responses:
            return self

        indices = [r.index for r in self.responses]
        if len(indices) != len(set(indices)):
            msg = "All indices must be unique."
            raise ValueError(msg)

        lengths = {len(r.responses) for r in self.responses}
        if len(lengths) > 1:
            msg = "All cells must have the same number of responses."
            raise ValueError(msg)

        return self


class ExperimentDatasetBase(BaseModel):
    """Schema for a complete dataset (prompts and responses).

    Attributes:
        prompts: A PromptDatasetBase object.
        responses: A ResponsesDatasetBase object.
    """

    prompts: PromptDatasetBase
    responses: ResponsesDatasetBase

    @model_validator(mode="after")
    def check_indices_match(self) -> "ExperimentDatasetBase":
        """Check that prompt and response indices match exactly."""
        prompt_indices = {p.index for p in self.prompts.prompts}
        response_indices = {r.index for r in self.responses.responses}

        if prompt_indices != response_indices:
            msg = "Prompt and response indices must match exactly."
            raise ValueError(msg)

        return self
