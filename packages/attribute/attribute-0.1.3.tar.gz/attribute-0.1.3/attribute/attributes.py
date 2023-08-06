import dataclasses
import typing


@dataclasses.dataclass
class Attribute:
    name: str

    def __getitem__(self, obj: typing.Any, /) -> typing.Any:
        return getattr(obj, self.name)

    def get(self, obj, default=None):
        return getattr(obj, self.name, default)

    def delete(self, obj) -> None:
        delattr(obj, self.name)

    def has(self, obj) -> bool:
        return hasattr(obj, self.name)

    def set(self, obj, val) -> None:
        setattr(obj, self.name, val)

    def setdefault(self, obj, default=None):
        if self.has(obj):
            return self.get(obj)

        self.set(obj, default)

        return default


@dataclasses.dataclass
class DefaultedAttribute(Attribute):
    factory: typing.Callable

    def setdefault(self, obj):
        return super().setdefault(obj, default=self.factory())

    def reset(self, obj):
        self.set(obj, self.factory())