from . import Pluggable
from wire.enums import Events
import typing
import inspect
import asyncio

class Eventable(Pluggable):
    def __init__(self) -> None:
        self.events: dict = {}

    def __call__(self, event: str) -> None:
        if isinstance(event, Events):
            event = event.value
        for function in self.events.get(event, []):
            if inspect.iscoroutinefunction(function):
                asyncio.run(function)
            else: 
                function()

    def add(self, event: typing.Union[Events, str] , function: typing.Callable) -> None:
        if isinstance(event, Events):
            event = event.value
        if function in self.events.get(event, []):
            return
        if event not in self.events.keys():
            self.events[event] = [function]
        else: 
            self.events[event].append(function)

