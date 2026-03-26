from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from src.auth.exceptions import AuthRequired, InvalidToken
from src.auth.schemas import JWTData
from src.config import settings

http_bearer = HTTPBearer(auto_error=False)


async def parse_jwt_user_data_optional(
    bearer: HTTPAuthorizationCredentials | None = Depends(http_bearer),
) -> JWTData | None:
    if not bearer:
        return None

    token = bearer.credentials

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except JWTError:
        raise InvalidToken()

    return JWTData(**payload)


async def parse_jwt_user_data(
    jwt_data: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> JWTData:
    if not jwt_data:
        raise AuthRequired()

    return jwt_data
