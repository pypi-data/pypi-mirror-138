from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from restful_starlette.apps.swagger.endpoint import docs_page, openapi_schema

routes = [
    # swagger文档地址
    Route(path='/docs', endpoint=docs_page, include_in_schema=False),
    # schema json输出地址
    Route(path='/schema.json', endpoint=openapi_schema, include_in_schema=False),
    # 静态资源包代理地址
    Mount(path='/swagger/static', app=StaticFiles(directory='statics', packages=['restful_starlette.apps.swagger', ]),
          name="swagger"),
]
