from starlette import status
from starlette.authentication import AuthenticationError
from starlette.requests import Request
from starlette.responses import Response
from tortoise.exceptions import BaseORMException, DoesNotExist

from restful_starlette.http.permissions import PermissionDeniedException
from restful_starlette.http.response import ResponseContentWrapperMixin


async def common_error_handler(request: Request, exc: Exception) -> Response:
    """
    公共错误处理方法，catch所有无法特殊处理的报错信息
    :param request:
    :param exc:
    :return:
    """
    return ResponseContentWrapperMixin().error(msg=exc.__str__(), code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def orm_error_handler(request: Request, exc: BaseORMException) -> Response:
    msg = "请求失败"
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    data = {
        'error_msg': exc.__str__(),
    }
    # 对部分orm error 进行特殊处理
    if isinstance(exc, DoesNotExist):
        code = status.HTTP_404_NOT_FOUND
        msg = "指定数据不存在"
    return ResponseContentWrapperMixin().error(msg=msg, code=code, data=data)


async def permission_error_handler(request: Request, exc: PermissionDeniedException) -> Response:
    msg = "权限不足"
    code = status.HTTP_403_FORBIDDEN
    return ResponseContentWrapperMixin().error(msg=msg, code=code, data={})


GLOBAL_EXCEPTION_HANDLERS = {
    Exception: common_error_handler,
    BaseORMException: orm_error_handler,
    PermissionDeniedException: permission_error_handler,
}
