import os

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from restful_starlette.apps.swagger.generator import CommonSchemaGenerator


def openapi_schema(request: Request):
    security = {
        # "oauth2": {
        #     "type": "oauth2",
        #     "flows": {
        #         "implicit": {
        #             "authorizationUrl": "/v1/oauth/authorize",
        #             "scopes": {
        #                 # "write:pets": "modify pets in your account",
        #                 # "read:pets": "read your pets"
        #                 "all": "all",
        #             },
        #         }
        #     }
        # },
        "api_key": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
    base = {"openapi": "3.0.0", "info": {"title": "Auth Service API", "version": "1.0"}}

    schemas = CommonSchemaGenerator(base_schema=base)

    app = getattr(request.app.state, 'top_app', request.app)

    schema = schemas.get_schema(app.routes)
    schema["components"].update({"securitySchemes": security})
    return JSONResponse(content=schema)
    # return schemas.OpenAPIResponse(request)


templates = Jinja2Templates(directory='restful_starlette/apps/swagger/statics')


def docs_page(request: Request):
    """
    docs page
    :param request:
    :return:
    """
    static_path = "." + os.path.join(request.app.prefix, "swagger/static")
    static_path.replace('//', '/')
    return templates.TemplateResponse('index.html', {'request': request, 'static_path': static_path})
    # return RedirectResponse(url='/static/statics/index.html')
