import inspect
import typing

import yaml
from pydantic.main import BaseModel
from pydantic.schema import schema
from starlette.routing import BaseRoute, Mount, Route, compile_path
from starlette.schemas import SchemaGenerator

from restful_starlette.http.endpoint import BaseHTTPEndpoint


class EndpointInfo(typing.NamedTuple):
    path: str
    http_method: str
    func: typing.Callable
    endpoint_class: typing.Union[typing.Type[BaseHTTPEndpoint], None] = None


class CommonSchemaGenerator(SchemaGenerator):
    """
        CommonSchemaGenerator
    """

    # self.components_schemas =

    def get_endpoints(
            self, routes: typing.List[BaseRoute]
    ) -> typing.List[EndpointInfo]:
        """
        Given the routes, yields the following information:

        - path
            eg: /users/
        - http_method
            one of 'get', 'post', 'put', 'patch', 'delete', 'options'
        - func
            method ready to extract the docstring
        """
        endpoints_info: list = []

        for route in routes:
            if isinstance(route, Mount):
                routes = route.routes or []
                sub_endpoints = []
                for sub_endpoint in self.get_endpoints(routes):
                    sub_endpoints.append(EndpointInfo(
                        path="".join((route.path, sub_endpoint.path)),
                        http_method=sub_endpoint.http_method,
                        func=sub_endpoint.func,
                        endpoint_class=sub_endpoint.endpoint_class,
                    ))

                endpoints_info.extend(sub_endpoints)

            elif not isinstance(route, Route) or not route.include_in_schema:
                continue

            elif inspect.isfunction(route.endpoint) or inspect.ismethod(route.endpoint):
                for method in route.methods or ["GET"]:
                    if method == "HEAD":
                        continue
                    endpoints_info.append(
                        EndpointInfo(route.path_format, method.lower(), route.endpoint)
                    )
            else:
                for method in ["get", "post", "put", "patch", "delete", "options"]:
                    if not hasattr(route.endpoint, method):
                        continue
                    func = getattr(route.endpoint, method)
                    if issubclass(route.endpoint, BaseHTTPEndpoint):
                        endpoints_info.append(
                            EndpointInfo(route.path_format, method.lower(), func, endpoint_class=route.endpoint)
                        )
                    else:
                        endpoints_info.append(
                            EndpointInfo(route.path_format, method.lower(), func)
                        )

        return endpoints_info

    def get_schema(self, routes: typing.List[BaseRoute]) -> dict:
        schema = dict(self.base_schema)
        schema.setdefault("paths", {})

        try:
            s = schema["components"]["schemas"]
        except Exception:
            schema.setdefault("components", {"schemas": {}})
        endpoints_info = self.get_endpoints(routes)

        self.models = set()
        self.component_schemas = {}

        for endpoint in endpoints_info:
            # print(endpoint)
            if endpoint.endpoint_class is not None:
                parsed = self.parse_endpoint_class(endpoint)
                self.get_components(endpoint)
            else:
                parsed = self.parse_docstring(endpoint.func)

            if not parsed:
                continue

            if endpoint.path not in schema["paths"]:
                schema["paths"][endpoint.path] = {}

            schema["paths"][endpoint.path][endpoint.http_method] = parsed

        schema["components"]["schemas"] = self.component_schemas

        return schema

    def parse_endpoint_class(self, endpoint: typing.ClassVar) -> dict:
        """
            Given a endpoint_class
        """
        parsed = {
            'summary': self.get_summary(endpoint),
            'description': self.get_description(endpoint),
            'tags': self.get_tags(endpoint),
            'operationId': self.get_operation_id(endpoint),
            'consumes': self.get_consumes(endpoint),
            'produces': self.get_produces(endpoint),
            'parameters': self.get_parameters(endpoint),
            'responses': self.get_responses(endpoint),
            'security': self.get_path_security(endpoint),
            # 'components': self.get_components(endpoint),
        }
        if endpoint.http_method != "get":
            parsed.update({'requestBody': self.get_request_body(endpoint), })

        return parsed

    def get_summary(self, endpoint: typing.ClassVar) -> str:
        parsed = self.load_from_docstring(endpoint.endpoint_class.__doc__)
        return parsed.get('summary', '')

    def get_description(self, endpoint: typing.ClassVar) -> str:
        parsed = self.load_from_docstring(endpoint.endpoint_class.__doc__)
        return parsed.get('description', '')

    def get_tags(self, endpoint: typing.ClassVar) -> typing.List:
        parsed = self.load_from_docstring(endpoint.endpoint_class.__doc__)
        return parsed.get('tags', [])

    def get_operation_id(self, endpoint: typing.ClassVar) -> str:
        return endpoint.endpoint_class.__name__

    def get_consumes(self, endpoint: typing.ClassVar) -> typing.List:
        result = [
            'application/json'
        ]
        # 优先从文档中获取
        parsed = self.load_from_docstring(endpoint.endpoint_class.__doc__)
        result = parsed.get('consumes', result)
        return result

    def get_produces(self, endpoint: typing.ClassVar) -> typing.List:
        result = [
            'application/json'
        ]
        # 优先从文档中获取
        parsed = self.load_from_docstring(endpoint.endpoint_class.__doc__)
        result = parsed.get('produces', result)
        return result

    def get_path_security(self, endpoint: typing.ClassVar) -> typing.List:

        if len(endpoint.endpoint_class.permission_classes) > 0:
            result = [
                {
                    "api_key": []
                }
            ]
        else:
            result = []
        # 优先从文档中获取
        parsed = self.load_from_docstring(endpoint.endpoint_class.__doc__)
        result = parsed.get('security', result)
        return result

    def get_path_params(self, endpoint: typing.ClassVar) -> typing.List:
        # 优先从文档中取参数结构
        path_params = []
        path_regex, path_format, param_convertors = compile_path(endpoint.path)
        for param in param_convertors.keys():
            path_params.append({
                "name": param,
                "in": "path",
                "description": "",
                "required": True,
            })
        return path_params

    def get_query_params(self, endpoint: typing.ClassVar) -> typing.List:
        path_params = []
        if endpoint.endpoint_class.request_class is None:
            return []

        fields = endpoint.endpoint_class.request_class.__fields__.keys()
        for param in fields:
            path_params.append({
                "name": param,
                "in": "query",
                "description": "",
                "required": False,
            })
        return path_params

    def get_request_body(self, endpoint: typing.ClassVar) -> typing.Dict:
        # 优先从文档中取参数结构
        _body = {
            "description": endpoint.endpoint_class.request_class.__doc__,
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": f"#/components/schemas/{endpoint.endpoint_class.request_class.__name__}"
                    }
                }
            },
            "required": True
        }

        return _body

    def get_parameters(self, endpoint: typing.ClassVar) -> typing.List:
        # 优先从文档中取参数结构
        # parsed = self.load_from_docstring(endpoint.endpoint_class.__doc__)
        # result = parsed.get('parameters', [])
        result = []
        result.extend(self.get_path_params(endpoint))
        if endpoint.http_method == "get":
            result.extend(self.get_query_params(endpoint))
        return result

    def get_responses(self, endpoint: typing.ClassVar) -> typing.Dict:
        # 优先从文档中取返回结构
        parsed = self.load_from_docstring(endpoint.endpoint_class.__doc__)
        result = parsed.get('responses', None)

        if result is not None:
            return result

        result = {}

        # response_schema_name = endpoint.endpoint_class.SUCCESS_RESPONSE_CLASS.__name__
        #
        # if response_schema_name not in self.component_schemas.keys():
        #     self.component_schemas[response_schema_name] = endpoint.endpoint_class.SUCCESS_RESPONSE_CLASS.schema(
        #         ref_template="#/components/schemas/")

        success_class = endpoint.endpoint_class.SUCCESS_RESPONSE_CLASS
        if success_class is not None and issubclass(success_class, BaseModel):
            self.models.add(success_class)

            success = endpoint.endpoint_class.SUCCESS_RESPONSE_CLASS()
            result[success.code] = {'description': success.message,
                                    "content": {"application/json": {
                                        "schema": {
                                            "$ref": f"#/components/schemas/{endpoint.endpoint_class.SUCCESS_RESPONSE_CLASS.__name__}"
                                        }
                                    },
                                        "application/xml": {
                                            "schema": {
                                                "$ref": f"#/components/schemas/{endpoint.endpoint_class.SUCCESS_RESPONSE_CLASS.__name__}"
                                            }
                                        }}}
        return result

    def get_components(self, endpoint: typing.ClassVar) -> typing.Dict:
        request = endpoint.endpoint_class.request_class
        response = endpoint.endpoint_class.response_class

        if request is not None and issubclass(request, BaseModel):
            self.models.add(request)

        if response is not None and issubclass(response, BaseModel):
            self.models.add(response)

        self.component_schemas = schema(self.models, ref_prefix='#/components/schemas/').get('definitions', {})
        return self.component_schemas

    def load_from_docstring(self, docstring: str = '') -> dict:
        """
        Given a docstring, parse the docstring as YAML and return a dictionary of info.
        """
        if not docstring:
            return {}

        assert yaml is not None, "`pyyaml` must be installed to use parse_docstring."

        # We support having regular docstrings before the schema
        # definition. Here we return just the schema part from
        # the docstring.
        docstring = docstring.split("---")[-1]

        parsed = yaml.safe_load(docstring)

        if not isinstance(parsed, dict):
            # A regular docstring (not yaml formatted) can return
            # a simple string here, which wouldn't follow the schema.
            return {}

        return parsed
