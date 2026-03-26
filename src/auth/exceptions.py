from src.auth.constants import ErrorCode
from src.exceptions import NotAuthenticated


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN
