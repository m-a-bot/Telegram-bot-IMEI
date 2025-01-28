from contextvars import ContextVar

from redis import Redis

from app.middlewares.di_middleware import DIMiddleware


class DIContainer:
    def __init__(self):
        self._dependencies = {}

    def provide(self, name: str, dependecy):
        self._dependencies[name] = dependecy

    def get(self, name: str):
        return self._dependencies.get(name)


container = DIContainer()
di_context: ContextVar[DIContainer] = ContextVar(
    "di_context", default=container
)

container.provide("get_db", Redis())


def get_dependency(name: str):
    return di_context.get().get(name)


di_middleware = DIMiddleware(di_context, container)
