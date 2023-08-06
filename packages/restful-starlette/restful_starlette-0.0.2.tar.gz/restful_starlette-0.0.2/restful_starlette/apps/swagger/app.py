from starlette.applications import Starlette

from restful_starlette.blueprint import Blueprint
from .routes import routes


class SwaggerBlueprint(Blueprint):

    def set_top_app(self, app: Starlette):
        setattr(self.state, "top_app", app)

    def install(self,
                app: Starlette,
                path: str = "/",
                name: str = None):
        self.set_top_app(app=app)


swagger = SwaggerBlueprint(routes=routes)
