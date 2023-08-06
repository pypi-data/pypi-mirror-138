import typing

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import BaseRoute
from starlette.types import ASGIApp


class Blueprint(Starlette):
    """
        Blue print class
        asgi class
    """

    def __init__(
            self,
            debug: bool = False,
            routes: typing.Sequence[BaseRoute] = None,
            middleware: typing.Sequence[Middleware] = None,
            exception_handlers: typing.Dict[
                typing.Union[int, typing.Type[Exception]], typing.Callable
            ] = None,
            on_startup: typing.Sequence[typing.Callable] = None,
            on_shutdown: typing.Sequence[typing.Callable] = None,
            lifespan: typing.Callable[["Starlette"], typing.AsyncContextManager] = None,
            prefix: str = '/'
    ) -> None:

        self.prefix = prefix

        super(Blueprint, self).__init__(debug=debug, routes=routes, middleware=middleware,
                                        exception_handlers=exception_handlers, on_startup=on_startup,
                                        on_shutdown=on_shutdown, lifespan=lifespan)

    def register(self,
                 app: typing.Union[typing.List[Starlette], Starlette],
                 path: str = "/",
                 name: str = None):
        """
        注册 blueprint
        :param app:
        :param path:
        :param name:
        :return:
        """

        if self.prefix != '/':
            path = self.prefix + path

        if isinstance(app, list):
            for application in app:
                application.pre_register()
                self.mount(path=path, name=name, app=application)
        else:
            self.mount(path=path, name=name, app=app)

    def install(self,
                app: Starlette,
                path: str = "/",
                name: str = None):
        pass


def register_blueprints(app: Blueprint,
                        blueprints: typing.List[Blueprint],
                        path: str = "/",
                        name: str = None):
    """
    注册 blueprint
    :param app:
    :param blueprints:
    :param path:
    :param name:
    :return:
    """

    if app.prefix != '/':
        path = app.prefix + path

    for application in blueprints:
        # 安装前有特殊处理逻辑通过执行install方法实现
        application.install(path=path, name=name, app=app)
        # 挂载应用
        app.mount(path=path, name=name, app=application)
