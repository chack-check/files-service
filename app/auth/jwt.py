import datetime

import msgspec
from jose import jwt

from ..settings import settings
from .exceptions import IncorrectToken
from .schemas import TokenUser

ALGORITHMS = ['HS256']


def decode_token(token: str) -> TokenUser:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=ALGORITHMS
        )
        assert payload['exp'] > datetime.datetime.now(datetime.timezone.utc).timestamp()
        decoded_sub = msgspec.json.decode(payload['sub'])
        assert 'user_id' in decoded_sub
        return TokenUser(**decoded_sub)
    except Exception:
        raise IncorrectToken
