from typing import Any

from pydantic import BaseModel, Field


class TaskRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class TaskResponse(BaseModel):

    task: str

    result: Any