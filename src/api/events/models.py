from sqlmodel import Field, SQLModel
from typing import Optional


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = ""
    description: Optional[str] = ""


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = ""


class EventUpdateSchema(SQLModel):
    description: str
    page: Optional[str] = None


class EventListSchema(SQLModel):
    results: list[EventModel]
    count: int
