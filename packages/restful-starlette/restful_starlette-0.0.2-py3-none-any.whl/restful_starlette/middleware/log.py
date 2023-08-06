import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = structlog.get_logger("request")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logging middleware."""

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        try:
            # body_json = await request.json()
            body_json = {}
        except Exception as ex:
            body_json = {}
        await logger.info("request", path=request.url.path, params=dict(request.query_params), body=body_json)
        return response
