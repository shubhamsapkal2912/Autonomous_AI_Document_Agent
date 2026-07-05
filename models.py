from pydantic import BaseModel, Field, field_validator


class AgentRequest(BaseModel):
    request: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        examples=[
            "Create a project proposal for implementing an AI chatbot for a retail company to improve customer support."
        ]
    )

    @field_validator("request")
    @classmethod
    def validate_request(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Request cannot be empty.")
        return value


class AgentResponse(BaseModel):
    status: str
    message: str
    document_path: str
    plan: list[str]
    assumptions: list[str]
    title: str
    document_type: str
    used_fallback: bool