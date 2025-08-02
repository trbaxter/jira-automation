from typing import runtime_checkable, Protocol


@runtime_checkable
class EnvReader(Protocol):
    """
    Represents a callable that retrieves values from environment variables.

    Intended to abstract access to repository secrets. Allows injection of
    mock implementations for testing and decouples environment access from
    core application logic.

    Implemented by default with 'os.getenv'.
    """

    def __call__(self, key: str) -> str | None: ...
