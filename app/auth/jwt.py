import datetime

import msgspec
from jose import jwt, JWTError

from .schemas import TokenUser
from .exceptions import IncorrectToken
from ..settings import settings


ALGORITHMS = ['HS256']


def decode_token(token: str) -> TokenUser:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=ALGORITHMS
        )
        assert payload['exp'] > datetime.datetime.utcnow().timestamp()
        decoded_sub = msgspec.json.decode(payload['sub'])
        assert 'user_id' in decoded_sub
        return TokenUser(**decoded_sub)
    except (AssertionError, KeyError, JWTError):
        raise IncorrectToken
