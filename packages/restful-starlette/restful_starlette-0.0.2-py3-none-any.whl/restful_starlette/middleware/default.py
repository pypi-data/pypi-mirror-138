from starlette.middleware import Middleware

from starlette.middleware.cors import CORSMiddleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from restful_starlette.middleware.log import LoggingMiddleware

DEFAULT_MIDDLEWARES = [
    Middleware(
        RawContextMiddleware,
        plugins=(
            plugins.CorrelationIdPlugin(),
            plugins.RequestIdPlugin(),
        ),
    ),
    Middleware(CORSMiddleware, allow_origins=['*']),

    Middleware(LoggingMiddleware),
]
