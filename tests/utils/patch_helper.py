from typing import Callable


def make_base_path(prefix: str) -> Callable[[str], str]:
    def base_path(name: str) -> str:
        return f"{prefix}.{name}"

    return base_path
