import typing

DEFAULT: object = object()

class Attribute:
    name: str
    __default: typing.Any = None
    __default_factory: typing.Optional[typing.Callable] = None

    def __init__(self, name: str, *, default: typing.Any = None, default_factory: typing.Optional[typing.Callable] = None) -> None:
        if default is not None and default_factory is not None:
            raise ValueError('cannot specify both default and default_factory')

        self.name = name
        self.__default = default
        self.__default_factory = default_factory

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.name!r}, default={self.default!r})'

    def __str__(self) -> str:
        return self.name

    @property
    def default(self) -> typing.Any:
        if self.__default_factory is not None:
            return self.__default_factory()

        return self.__default

    def __getitem__(self, obj: typing.Any, /) -> typing.Any:
        return getattr(obj, self.name)

    def get(self, obj: typing.Any, default: typing.Any=DEFAULT) -> typing.Any:
        return getattr(obj, self.name, default if default is not DEFAULT else self.default)

    def delete(self, obj: typing.Any) -> None:
        delattr(obj, self.name)

    def has(self, obj: typing.Any) -> bool:
        return hasattr(obj, self.name)

    def set(self, obj: typing.Any, val: typing.Any=DEFAULT) -> None:
        setattr(obj, self.name, val if val is not DEFAULT else self.default)

    def setdefault(self, obj: typing.Any, default: typing.Any=DEFAULT) -> typing.Any:
        if self.has(obj):
            return self.get(obj)

        self.set(obj, default if default is not DEFAULT else self.default)

        return self.get(obj)