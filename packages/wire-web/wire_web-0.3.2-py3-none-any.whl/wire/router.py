from wire_rxtr import RadixTree
import typing

class BaseRouter:
    """
    Here is the routing magic.
    """
    __slots__ = ["routes"]

    def __init__(self, strict: bool = True) -> None:
        self.strict_mode: bool = strict
        self.routes = RadixTree()

    def add_route(self, path: str, handler, method: str, dependencies: list = []) -> bool:
        if not self.strict_mode:
            path = path[:-1] if path.endswith("/") and len(path) > 1 else path
        self.routes.insert(path, handler, method, dependencies)
        return True


class Router(BaseRouter):
    def __init__(self, strict: bool = True):
        super().__init__(strict=strict)

    async def get_handler(self, path: str, method: str) -> typing.Tuple[
        typing.Union[typing.Callable, typing.Awaitable], typing.Optional[dict]]:
        if not self.strict_mode:
            path = path[:-1] if path.endswith("/") and len(path) > 1 else path
        pathFound, handler, params, dependencies = self.routes.get(path, method)
        return handler, params, dependencies
