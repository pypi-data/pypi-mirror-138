import time
import typing
from dataclasses import dataclass, field, asdict
from enum import Enum

import jwt


class TokenType(str, Enum):
    Bearer = "bearer"
    AccessToken = "access_token"
    RefreshToken = "refresh_token"


class JsonWebToken(typing.NamedTuple):
    token_type: TokenType
    access_token: str
    refresh_token: str
    expire_in: int


class JWT:

    def __init__(self, secret: str = "aaxx", algorithm: str = "HS256", expire: int = 86400 * 3):
        self.secret = secret
        self.algorithm = algorithm
        self.expire = expire
        self.refresh_token_expire = self.expire + expire

    def generate_jwt(self, token_type: TokenType, payload: typing.Dict) -> JsonWebToken:
        # 初始化并更新payload
        iat = int(time.time())
        _payload = {
            "token_type": token_type.value,
            "iat": iat,
            "exp": iat + self.expire,
        }
        _payload.update(payload)

        # 生成access token
        access_token = self.encode(_payload)

        # 重新构建refresh token
        refresh_payload = _payload.copy()
        refresh_payload.update(
            _payload={
                "token_type": TokenType.RefreshToken.value,
                "exp": iat + self.refresh_token_expire,
            }
        )
        # 生成refresh token
        refresh_token = self.encode(refresh_payload)

        return JsonWebToken(token_type=token_type,
                            access_token=access_token,
                            refresh_token=refresh_token,
                            expire_in=iat + self.expire)

    def encode(self, payload: typing.Dict) -> str:
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode(self, encoded) -> typing.Dict:
        return jwt.decode(encoded, self.secret, algorithms=[self.algorithm])