from typing import runtime_checkable, Protocol

from src.customtypes.shared import NonEmptyStr


@runtime_checkable
class EnvReader(Protocol):
    def __call__(
            self,
            key: str,
            default: str | None = None
    ) -> NonEmptyStr | None:
        ...
