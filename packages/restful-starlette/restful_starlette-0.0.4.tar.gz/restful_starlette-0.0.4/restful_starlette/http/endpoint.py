import asyncio
import typing
from typing import Dict, Type, Union

from pydantic import BaseModel, Field
from starlette import status
from starlette.authentication import requires, AuthenticationError
from starlette.concurrency import run_in_threadpool
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import Response
from tortoise import Model
from tortoise.contrib.pydantic import pydantic_queryset_creator
from tortoise.models import MODEL
from tortoise.queryset import QuerySet, QuerySetSingle
from tortoise.transactions import atomic

from restful_starlette.http.permissions import BasePermission, PermissionDeniedException, \
    IsAuthenticated
from restful_starlette.http.response import ResponseContentWrapperMixin, EmptyData
from restful_starlette.http.restful import CreateViewMixin, RetrieveViewMixin, ListViewMixin, UpdateViewMixin, \
    DestroyViewMixin
from restful_starlette.http.transport import HTTPTransport
from restful_starlette.orm.tortoise_orm import ActiveStatusEnum


class BaseHTTPEndpoint(HTTPEndpoint, HTTPTransport, ResponseContentWrapperMixin):
    """
    BaseHTTPEndpoint
    """
    permission_classes: typing.List[typing.Type[BasePermission]] = [IsAuthenticated, ]

    @atomic()
    async def dispatch(self) -> None:
        request = Request(self.scope, receive=self.receive)
        handler_name = "get" if request.method == "HEAD" else request.method.lower()
        handler = getattr(self, handler_name, self.method_not_allowed)
        is_async = asyncio.iscoroutinefunction(handler)

        result = await self.has_permissions(request)
        if not result:
            raise PermissionDeniedException("permission denied")

        if is_async:
            response = await handler(request)
        else:
            response = await run_in_threadpool(handler, request)
        await response(self.scope, self.receive, self.send)

    def mock_response(self, type: str = 'success') -> typing.Dict:
        if type == 'success':
            result = self.SUCCESS_RESPONSE_CLASS().dict()
        elif type == 'fail':
            result = self.FAIL_RESPONSE_CLASS().dict()
        else:
            result = self.ERROR_RESPONSE_CLASS().dict()
        return result

    async def has_permissions(self, request: Request) -> bool:
        for permission_class in self.permission_classes:
            permission = permission_class()
            is_async = asyncio.iscoroutinefunction(permission.has_permission)
            if is_async:
                result = await permission.has_permission(request)
            else:
                result = await run_in_threadpool(permission.has_permission, request)
            if not result:
                return False
        return True


class ModelViewSetMixin:
    """
        mixin class which suit for Tortoise-orm model
    """
    model: Model
    look_field: str = 'id'

    async def get_instance(self, request: Request) -> MODEL:
        look_value = request.path_params.get(self.look_field, None)
        return await self.model.get(**{self.look_field: look_value})

    def get_queryset(self) -> QuerySet[MODEL]:
        return self.model.filter(is_active=ActiveStatusEnum.ACTIVE)

    def filter_queryset(self, queryset: QuerySet[MODEL]) -> QuerySet[MODEL]:
        return queryset


class CreateHTTPEndpoint(BaseHTTPEndpoint, CreateViewMixin, ModelViewSetMixin):

    async def create(self, request: Request) -> Response:
        in_obj = self.decode_request(request_obj=await request.json())
        new_instance = await self.model.create(**in_obj.dict())
        out_obj = self.response_class.parse_obj(new_instance)
        return self.success(msg="创建成功", data=out_obj).all()


class RetrieveHTTPEndpoint(BaseHTTPEndpoint, RetrieveViewMixin, ModelViewSetMixin):

    async def retrieve(self, request: Request) -> Response:
        instance = await self.get_instance(request=request)
        if instance is None:
            return self.fail(code=status.HTTP_404_NOT_FOUND, msg='指定记录不存在')
        out_obj = self.response_class.parse_obj(instance)
        return self.success(msg="请求成功", data=out_obj)


class ListHTTPEndpoint(BaseHTTPEndpoint, ListViewMixin, ModelViewSetMixin):

    async def list(self, request: Request) -> Response:
        in_obj = self.decode_request(request_obj=dict(request.query_params))
        queryset = self.filter_queryset(self.get_queryset())
        instances = await queryset
        out_objs = [self.response_class.parse_obj(obj) for obj in instances]
        return self.success(msg="请求成功", data=out_objs)


class UpdateHTTPEndpoint(BaseHTTPEndpoint, UpdateViewMixin, ModelViewSetMixin):

    async def update(self, request: Request) -> Response:
        in_obj = self.decode_request(request_obj=dict(request.query_params))

        instance = await self.get_instance(request=request)
        if instance is None:
            return self.fail(code=status.HTTP_404_NOT_FOUND, msg='指定记录不存在')
        instance.update_from_dict(in_obj.dict())
        await instance.save()
        out_obj = self.response_class.parse_obj(instance)
        return self.success(msg="更新成功", data=out_obj)


class DestroyHTTPEndpoint(BaseHTTPEndpoint, DestroyViewMixin, ModelViewSetMixin):

    async def destroy(self, request: Request) -> Response:
        instance = await self.get_instance(request=request)
        if instance is None:
            return self.fail(code=status.HTTP_404_NOT_FOUND, msg='指定记录不存在')
        await instance.update(is_active=ActiveStatusEnum.DEACTIVE.value)
        return self.success(msg="删除成功", data=EmptyData())
