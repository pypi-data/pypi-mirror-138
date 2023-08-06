import typing

from starlette import status
from starlette.authentication import BaseUser, AuthenticationBackend, AuthenticationError, AuthCredentials
from starlette.requests import Request
from starlette.responses import Response

from micro_kits.oauth.objects import UserObject, ClientObject
from restful_starlette.utils.jwt import TokenType
from restful_starlette.http.response import ResponseContentWrapperMixin
from micro_kits.oauth.storage import ObjectStorage


def authenticate_error_handler(request: Request, exc: AuthenticationError) -> Response:
    msg = "认证失败"
    code = status.HTTP_401_UNAUTHORIZED
    return ResponseContentWrapperMixin().error(msg=msg, code=code, data={})


class UserSubject(BaseUser):

    def __init__(self, uid: str, username: str, name: str = "", is_client: bool = False,
                 meta: typing.Any = None) -> None:
        self.username = username
        self.name = name
        self.uid = uid
        self.is_client = is_client
        self.meta = meta

    @property
    def identity(self) -> str:
        return self.uid

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.name


class JWTAuthBackend(AuthenticationBackend):
    """
    Basic Usage:
        Middleware(AuthenticationMiddleware, backend=JWTAuthBackend(storage), on_error=authenticate_error_handler)
    """

    def __init__(self, storage: ObjectStorage) -> None:
        self.storage = storage

    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            is_valid = await self.validate_token(credentials)

            token_types = [e.lower() for e in TokenType]
            if scheme.lower() not in token_types or not is_valid:
                return
            decoded = await self.storage.inspect_token(credentials)
        except Exception as exc:
            raise AuthenticationError('Invalid auth credentials')

        auth_obj = await self.get_auth_obj(decoded)
        if auth_obj is None:
            return
        is_client = isinstance(auth_obj, ClientObject)
        auth_credentials = ["authenticated"]
        if is_client:
            auth_credentials.append('is_client')
        return AuthCredentials(auth_credentials), UserSubject(uid=auth_obj.uid,
                                                              name=auth_obj.name,
                                                              username=getattr(auth_obj, 'username', auth_obj.name),
                                                              is_client=is_client,
                                                              meta=auth_obj)

    # def set_auth_object_to_context(self, auth_obj: typing.Union[UserObject, ClientObject]):
    #     if isinstance(auth_obj, UserObject):
    #         context.set('user', auth_obj)
    #     elif isinstance(auth_obj, ClientObject):
    #         context.set('client', auth_obj)

    async def get_auth_obj(self, token_info) -> typing.Union[UserObject, ClientObject, None]:
        if TokenType.Bearer == token_info.get("token_type"):
            auth_obj = await self.storage.get_user_by_identity(identity=token_info.get('uid', ''))
        elif TokenType.AccessToken == token_info.get("token_type"):
            auth_obj = await self.storage.get_client_by_identity(identity=token_info.get('uid', ''))
        else:
            auth_obj = None
        return auth_obj

    async def validate_token(self, token) -> bool:
        return await self.storage.validate_token(token)
