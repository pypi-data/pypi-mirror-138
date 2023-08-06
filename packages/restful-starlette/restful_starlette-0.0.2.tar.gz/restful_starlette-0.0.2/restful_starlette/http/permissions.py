from starlette.requests import Request


class PermissionDeniedException(Exception):
    pass


class BasePermission:

    async def has_permission(self, request: Request) -> bool:
        raise NotImplementedError()


class IsAuthenticated(BasePermission):

    async def has_permission(self, request: Request) -> bool:
        return request.user.is_authenticated


class IsUser(BasePermission):

    async def has_permission(self, request: Request) -> bool:
        return not request.user.is_client
