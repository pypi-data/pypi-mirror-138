from typing import Any, Tuple


def prod_cert(*args: Any, **kwargs: Any) -> Tuple[bool, Any]:
    return (False, None)


def stg_cert(*args: Any, **kwargs: Any) -> Tuple[bool, Any]:
    return (False, None)
