from enum import IntEnum
from typing import Type, List, Union, Any, Dict

from pydantic import BaseModel, Field
from starlette import status
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse


class StateEnum(IntEnum):
    """
        用于表示业务逻辑状态的枚举类
    """
    OK = 1
    BROKEN = 2


class EmptyData(BaseModel):
    """

    """


class SuccessResponse(BaseModel):
    message: str = '请求成功'
    code: int = status.HTTP_200_OK
    state: int = StateEnum.OK.value
    # data: Union[BaseModel, List[BaseModel]] = Field(default=EmptyData())
    data: Any = Field(default=EmptyData())


class FailResponse(BaseModel):
    message: str = '请求失败'
    code: int = status.HTTP_400_BAD_REQUEST
    state: int = StateEnum.BROKEN.value
    # data: Union[BaseModel, List[BaseModel]] = Field(default=EmptyData())
    data: Any = Field(default=EmptyData())


class ErrorResponse(BaseModel):
    message: str = '系统异常'
    code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    state: int = StateEnum.BROKEN.value
    # data: Union[BaseModel, List[BaseModel]] = Field(default=EmptyData())
    data: Any = Field(default=EmptyData())


class ResponseContentWrapperMixin:
    SUCCESS_RESPONSE_CLASS = SuccessResponse
    FAIL_RESPONSE_CLASS = FailResponse
    ERROR_RESPONSE_CLASS = ErrorResponse

    def success(self, msg: str = "请求成功", code: int = status.HTTP_200_OK, state: int = StateEnum.OK,
                data: Union[BaseModel, List[BaseModel], Dict] = EmptyData(), background: BackgroundTask = None):
        return JSONResponse(content=self.SUCCESS_RESPONSE_CLASS(message=msg, code=code, state=state, data=data).dict(),
                            background=background)

    def fail(self, msg: str = "请求失败", code: int = status.HTTP_400_BAD_REQUEST, state: int = StateEnum.BROKEN,
             data: Union[BaseModel, List[BaseModel], Dict] = EmptyData(), background: BackgroundTask = None):
        return JSONResponse(content=self.FAIL_RESPONSE_CLASS(message=msg, code=code, state=state, data=data).dict(),
                            background=background)

    def error(self, msg: str = "系统异常", code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, state: int = StateEnum.BROKEN,
              data: Union[BaseModel, List[BaseModel], Dict] = EmptyData(), background: BackgroundTask = None):
        return JSONResponse(content=self.ERROR_RESPONSE_CLASS(message=msg, code=code, state=state, data=data).dict(),
                            background=background)
