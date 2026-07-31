"""Data schema definitions for prismal."""

from pydantic import BaseModel, Field, model_validator


class PromptRowBase(BaseModel):
    """Base model for a single prompt row.

    Attributes:
        index: A unique dataset-level identifier for the prompt.
        prompt: The actual prompt text.
    """

    index: int = Field(..., description="A unique identifier for the prompt.")
    prompt: str = Field(..., description="The prompt string.")


class ResponsesRowBase(BaseModel):
    """Base model for a single response row.

    Attributes:
        index: A unique identifier for the response, corresponding to a prompt index.
        responses: A list of all response strings generated for the prompt.
    """

    index: int = Field(..., description="A unique identifier for the response.")
    responses: list[str] = Field(..., description="A list of response strings.")

    @property
    def response(self) -> str:
        """Get the first response string.

        Returns:
            The first response string, or an empty string if no responses exist.
        """
        return self.responses[0] if self.responses else ""


class PromptDatasetBase(BaseModel):
    """Schema for a collection of prompts.

    This model ensures that all prompts in the collection have unique indices.

    Attributes:
        prompts: A list of PromptRowBase objects.
    """

    prompts: list[PromptRowBase]

    @model_validator(mode="after")
    def check_unique_index(self) -> "PromptDatasetBase":
        """Validate that all prompt indices are unique.

        Returns:
            The validated PromptDatasetBase instance.

        Raises:
            ValueError: If duplicate indices are found.
        """
        indices = [p.index for p in self.prompts]
        if len(indices) != len(set(indices)):
            msg = "All indices must be unique."
            raise ValueError(msg)
        return self


class ResponsesDatasetBase(BaseModel):
    """Schema for a collection of responses.

    This model ensures that all responses have unique indices and that each
    row contains the same number of responses.

    Attributes:
        responses: A list of ResponsesRowBase objects.
    """

    responses: list[ResponsesRowBase]

    @model_validator(mode="after")
    def check_schema_consistency(self) -> "ResponsesDatasetBase":
        """Check for unique indices and consistent response counts across rows.

        Returns:
            The validated ResponsesDatasetBase instance.

        Raises:
            ValueError: If duplicate indices are found or if response counts
                are inconsistent.
        """
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
    """Schema for a complete experiment dataset.

    An experiment dataset consists of both prompts and their corresponding
    responses, with matching indices.

    Attributes:
        prompts: A collection of prompts.
        responses: A collection of responses.
    """

    prompts: PromptDatasetBase
    responses: ResponsesDatasetBase

    @model_validator(mode="after")
    def check_indices_match(self) -> "ExperimentDatasetBase":
        """Ensure that prompt and response indices match exactly.

        Returns:
            The validated ExperimentDatasetBase instance.

        Raises:
            ValueError: If there is a mismatch between prompt and response indices.
        """
        prompt_indices = {p.index for p in self.prompts.prompts}
        response_indices = {r.index for r in self.responses.responses}

        if prompt_indices != response_indices:
            msg = "Prompt and response indices must match exactly."
            raise ValueError(msg)

        return self
