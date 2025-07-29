from typing import runtime_checkable, Protocol


@runtime_checkable
class EnvReader(Protocol):
    """
    Serves as a type-safe contract for injecting environment values rather
    than relying on hard-coded usages of 'os.getenv'.

    Uses '...' to indicate that no class body is required to function.
    """

    def __call__(self, key: str) -> str: ...
