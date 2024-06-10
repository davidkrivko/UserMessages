from pydantic import BaseModel


class MessageCreate(BaseModel):
    bot_token: str
    chat_id: str
    message: str
