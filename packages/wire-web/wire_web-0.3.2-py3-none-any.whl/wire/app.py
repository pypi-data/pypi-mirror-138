from wire.groups.group import Group
from wire.plugs import Pluggable
from wire.plugs.alternator import Alternator
from wire.router import Router
from wire.request import Request
from wire.static import StaticFiles
from wire.listener import EventListener
from wire.enums import Events
import inspect
import typing
import traceback

class Wire:
    def __init__(
        self,
        title: str = "Wire APP",
        description: str = "",
        strict: bool = False,
    ) -> None:
        self.title: str = title
        self.description: str = description
        self.router: Router = Router(strict=strict)
        self.__event_listener: EventListener = EventListener()
        self.alternator = Alternator()

    async def __call__(self, scope: dict, receive, send) -> None:
        # lifespan handling
        try:
            if scope["type"] == "lifespan":
                while True:
                    message = await receive()
                    if message['type'] == 'lifespan.startup':
                        self.__event_listener(Events.ASGI_STARTUP)
                        await send({'type': 'lifespan.startup.complete'})
                    elif message['type'] == 'lifespan.shutdown':
                        self.__event_listener(Events.ASGI_STARTUP)
                        await send({'type': 'lifespan.shutdown.complete'})
                        return
            else:
                req = Request(scope, receive, send)
                func, params, deps = await self.router.get_handler(req.path, req.method)
                resp = await self.alternator(req, func, params, deps)
                await resp(scope, receive, send)
        except:
            traceback.print_exc()
            await send({'type': 'http.response.start', 'status': 500})
            await send({'type': 'http.response.body', 'body': b"Internal Server Error"})
                
                    

    def get(self, path: str, dependencies: list = []):
        def wrapper(handler: typing.Callable) -> typing.Callable:
            self.router.add_route(path, handler, "get", dependencies)
            return handler

        return wrapper

    def post(self, path: str, dependencies: list = []):
        def wrapper(handler: typing.Callable) -> typing.Callable:
            self.router.add_route(path, handler, "post", dependencies)
            return handler

        return wrapper

    def put(self, path: str, dependencies: list = []):
        def wrapper(handler: typing.Callable) -> typing.Callable:
            self.router.add_route(path, handler, "put", dependencies)
            return handler

        return wrapper

    def delete(self, path: str, dependencies: list = []):
        def wrapper(handler: typing.Callable) -> typing.Callable:
            self.router.add_route(path, handler, "delete", dependencies)
            return handler

        return wrapper

    def mount(self, plugin: Pluggable, prefix: str = None) -> bool:
        self.__event_listener(Events.PLUGIN_MOUNT)
        if not prefix.startswith("/"):
            raise Exception(f"Invalid prefix for router {plugin}")
        if isinstance(plugin, StaticFiles):
            self.router.add_route(prefix + "/*filename", plugin, "get")
            self.__event_listener(Events.STATIC_MOUNT)
            return True
        if isinstance(plugin, Group):
            for route in plugin.routes:
                path, handler, method, dependencies = route
                if not self.router.strict_mode and path.startswith("/"):
                    path = path[:-1]

                self.router.add_route(prefix + path, handler, method, dependencies)
            self.__event_listener(Events.GROUP_MOUNT)
            return True
            
    
    def event(self, event: str) -> None:
        def wrapper(handler: typing.Union[typing.Callable, typing.Awaitable]) -> None:
            self.__event_listener.add(event, handler)
            return handler

        return wrapper
