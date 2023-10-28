from typing import Annotated

from fastapi import Security, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .exceptions import IncorrectToken
from .schemas import TokenUser
from .jwt import decode_token


oauth2_scheme = HTTPBearer(auto_error=False)


def current_user(
        credentials: Annotated[HTTPAuthorizationCredentials | None,
                               Security(oauth2_scheme)]) -> TokenUser | None:
    if not credentials:
        return None

    token = credentials.credentials
    try:
        user = decode_token(token)
    except IncorrectToken:
        return None

    return user


def auth_required(user: Annotated[TokenUser | None, Depends(current_user)]) -> TokenUser:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect token")

    return user

