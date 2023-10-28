from pydantic import BaseModel


class TokenUser(BaseModel):
    user_id: int
    username: str

