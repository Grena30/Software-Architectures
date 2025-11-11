from typing import Optional
from sqlmodel import SQLModel, Field


class PredictServices(SQLModel):
    service_type: str = Field(default="")
    endpoint: str = Field(default="")
    model: str = Field(default="")
    version: str = Field(default="")
