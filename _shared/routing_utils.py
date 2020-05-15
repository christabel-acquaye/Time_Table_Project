import logging as logger
from functools import partial, wraps
from typing import Any, Callable, List

from flask import Flask, jsonify, make_response

from . import use_schema
from .typings import HTTP_METHODS, RouterParams
from .utilities import with_key


def with_response(func: Any, status_code: int):
    """ serialize api response """

    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        logger.debug(f'response {response}')
        return make_response(jsonify(response), status_code)

    return wrapper


def with_router(**params: RouterParams):
    """ configure route """

    method = params['method'] or HTTP_METHODS.GET
    schema = params.get('schema')
    status_code = params.get(
        'status_code') or 200 if method == HTTP_METHODS.GET else 201

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = partial(func, *args, **kwargs)
            handler = use_schema(schema, handler)
            handler = with_response(handler, status_code)
            return with_key(path=params['path'], method=method, handler=handler)

        return wrapper

    return decorator


def use_post(path: str, schema: Any = None):
    """ configure route as HTTP POST REQUEST """
    return with_router(**with_key(schema=schema, path=path, method=HTTP_METHODS.POST))


def use_get(path: str):
    """ configure route as HTTP GET REQUEST """
    return with_router(**with_key(path=path, method=HTTP_METHODS.GET))


def use_put(path: str, schema: Any):
    """ configure route as HTTP PUT REQUEST """
    return with_router(**with_key(schema=schema, path=path, method=HTTP_METHODS.PUT))


def use_delete(path: str, schema: Any):
    """ configure route as HTTP DELETE REQUEST """
    return with_router(**with_key(schema=schema, path=path, method=HTTP_METHODS.DELETE))


def add_route(app: Flask, basePath: str, path: str, handler: Callable, method: HTTP_METHODS):
    """ add route to flask apis """

    path = f'{basePath}{path}'
    app.add_url_rule(rule=path, view_func=handler,
                     methods=[method.value], endpoint=path)


def in_scope(app: Flask, basePath: str, handlers: List[Any]):
    """ group route in api scope """

    for child in handlers:
        add_route(app=app, basePath=basePath, **child())
