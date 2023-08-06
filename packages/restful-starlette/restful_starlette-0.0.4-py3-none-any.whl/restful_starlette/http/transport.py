from typing import Dict, Type, Union
from pydantic import BaseModel


class DefaultRequest(BaseModel):
    ...


class DefaultResponse(BaseModel):
    ...


class BaseTransport:
    """
    BaseTransport
    """

    # 入参类，集成自pydantic.BaseModel
    request_class: Union[BaseModel, None] = DefaultRequest
    # 出参类，集成自pydantic.BaseModel
    response_class: Union[BaseModel, None] = DefaultResponse

    def encode_request(self, request_obj: Union[BaseModel, None]) -> Dict:
        """
        对请求对象进行检查并编码成dict
        :param request_obj:
        :return:
        """
        if isinstance(request_obj, type(self.request_class)):
            return request_obj.dict()
        else:
            return {}

    def decode_request(self, request_obj: Union[Dict, None]) -> Type[response_class]:
        """
        对请求进行解码，并转化为指定的请求类型
        :param request_obj:
        :return:
        """
        return self.request_class.parse_obj(request_obj)

    def encode_response(self, response_obj: Union[BaseModel, None]) -> Dict:
        """
        对响应对象进行检查并编码成dict
        :param response_obj:
        :return:
        """
        if isinstance(response_obj, type(self.response_class)):
            return response_obj.dict()
        else:
            return {}

    def decode_response(self, request_obj: Union[Dict, None]) -> Union[BaseModel, None]:
        """
        对响应进行解码，并转化为指定的响应类型
        :param request_obj:
        :return:
        """
        if request_obj is None:
            return None
        else:
            return self.request_class.parse_obj(request_obj)


class HTTPTransport(BaseTransport):
    """
        transport for common http service
    """
