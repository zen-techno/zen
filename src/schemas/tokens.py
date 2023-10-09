from pydantic import BaseModel


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str
