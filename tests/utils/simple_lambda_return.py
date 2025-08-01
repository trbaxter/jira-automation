from typing import Any, Callable


def lambda_return(val) -> Callable[..., Any]:
    return lambda *_, **__: val