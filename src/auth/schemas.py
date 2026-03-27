from pydantic import Field

from src.schemas import CustomModel


class JWTData(CustomModel):
    user_id: str = Field(alias="sub")
    name: str
    iat: int
