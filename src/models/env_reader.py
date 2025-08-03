from typing import runtime_checkable, Protocol


@runtime_checkable
class EnvReader(Protocol):
    def __call__(self, key: str) -> str | None: ...
