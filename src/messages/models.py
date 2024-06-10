from sqlalchemy import JSON, Column
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, Dict
from datetime import datetime


class MessageDB(SQLModel, table=True):
    __tablename__ = "messages"

    id: int = Field(default=None, primary_key=True, index=True)
    bot_token: str = Field()
    chat_id: str = Field()
    message: str
    response: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    user_id: int = Field(foreign_key="users.id", index=True)
    timestamp: datetime = Field(default_factory=datetime.now)

    author: Optional["CustomUsersDB"] = Relationship(back_populates="request_logs")
