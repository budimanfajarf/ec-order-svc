from pydantic import Field

from src.schemas import CustomModel


class JWTData(CustomModel):
    user_id: int = Field(alias="sub")
    name: str
    iat: int
