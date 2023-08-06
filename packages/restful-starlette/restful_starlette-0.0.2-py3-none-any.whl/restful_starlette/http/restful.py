from starlette.requests import Request
from starlette.responses import Response


class CreateViewMixin:

    async def create(self, request: Request) -> Response:
        raise NotImplementedError()

    async def post(self, request: Request) -> Response:
        return await self.create(request=request)


class RetrieveViewMixin:

    async def retrieve(self, request: Request) -> Response:
        raise NotImplementedError()

    async def get(self, request: Request) -> Response:
        return await self.retrieve(request=request)


class ListViewMixin:

    async def list(self, request: Request) -> Response:
        raise NotImplementedError()

    async def get(self, request: Request) -> Response:
        return await self.list(request=request)


class UpdateViewMixin:

    async def update(self, request: Request) -> Response:
        raise NotImplementedError()

    async def put(self, request: Request) -> Response:
        return await self.update(request=request)

    async def patch(self, request: Request) -> Response:
        setattr(request, 'is_patch_update', True)
        return await self.update(request=request)


class DestroyViewMixin:

    async def destroy(self, request: Request) -> Response:
        raise NotImplementedError()

    async def delete(self, request: Request) -> Response:
        return await self.destroy(request=request)
