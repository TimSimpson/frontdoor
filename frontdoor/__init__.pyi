import typing as t

import mypy_extensions as mt




FrontDoorFunc = t.Union[
    t.Callable[[t.List[str]], int],
    t.Callable[[t.List[str]], None],
    t.Callable[[], int],
    t.Callable[[], None]
]

F = t.TypeVar('F', bound=FrontDoorFunc)


CommandData = mt.TypedDict("CommandData", {
    'fn': FrontDoorFunc,
    'desc': str,
    'help': t.Optional[str],
    'show': bool,
    'visible_name': str,
})


def from_root(path: str) -> str: ...


class CommandRegistry(object):

    commands: t.Dict[str, CommandData]
    name: str

    def __init__(self, name: str) -> None: ...

    def decorate(self, name: t.Union[str, t.List[str]], desc: str='', help: t.Optional[str]=None) -> t.Callable[[F], F]: ...

    def dispatch(self, args: t.List[str]) -> int: ...

    def help(self, args: t.List[str]) -> int: ...
