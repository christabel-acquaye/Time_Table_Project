from enum import Enum
from typing import Any, Union

try:
    # Python < 3.8
    # pip install mypy_extensions
    from mypy_extensions import TypedDict
except ImportError:
    # Python 3.8
    from typing import TypedDict


class IError(TypedDict):
    message: str
    data: Union[dict, None]
    status: Union[int, None]
    errors: Union[list, None]
    response: Union[Any, None]


class HTTP_METHODS(Enum):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PUT = 'PUT'


class RouterParams(TypedDict):
    method: Union[HTTP_METHODS, None]
    path: str
    schema: Union[Any, None]
    code: Union[int, None]

class AuthProvider(Enum):
    LOCAL = 'LOCAL'
    GOOGLE = 'GOOGLE'
    APPLE = 'APPLE'
    FACEBOOK = 'FACEBOOK'