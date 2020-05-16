import logging as logger
from functools import partial, wraps
from typing import Callable, Dict, List, Union

from _shared.error_service import JSON_VALIDATION_ERROR
from flask import request
from jsonschema import ValidationError, validate


def use_schema(schema: Union[Dict, List], func: Callable):
    """schema validation middleware

    Arguments:
            schema {Union[Dict, List]} -- json schema definition
            func {Callable} -- wrapped function

    Raises:
            JSON_VALIDATION_ERROR: [description]

    Returns:
            Callable -- decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """validates request payload with the jsonschema

        Raises:
                JSON_VALIDATION_ERROR: Json validation error

        Returns:
                any -- results of wrapped function
        """
        data = request.get_json()
        logger.debug(f'payload {data}')
        if schema:
            try:
                validate(instance=data, schema=schema)
            except ValidationError as error:
                try:
                    error_details = {
                        'path': '/'.join([
                                str(p) for p in list(error.absolute_path)[1::2]
                        ]),
                        'reason': error.message
                    }
                except IndexError:
                    error_details = {'path': '', 'message': error.message}
                raise JSON_VALIDATION_ERROR(error_details)
        return func(*args, **kwargs)

    return wrapper


def with_schema(schema: Union[Dict, List], inData=True):
    """wrapper for json schema

    Arguments:
            schema {Union[Dict, List]} -- json schema definition

    Keyword Arguments:
            inData {bool} -- is schema nested in data (default: {True})

    Returns:
            Dict -- wrapped schema
    """

    if not inData:
        return {**schema, 'additionalProperties': False}

    return {
        'type': 'object',
        'properties': {'data': schema},
        'required': ['data']
    }


def with_object(**kwargs):
    """Defines if schema is an object type schema

    Returns:
            Dict -- wrapped schema
    """
    return with_schema({
        'type': 'object', 'properties': kwargs['properties'],
        'required': kwargs.get('required', [])},
        kwargs.get('inData', [])
    )


def with_array(items, inData=False):
    """defines if schema is of array type

    Arguments:
            items {List} -- schema definition

    Keyword Arguments:
            inData {bool} -- is schema nested in data (default: {False})

    Returns:
            Dict -- wrapped schema
    """
    return with_schema({'type': 'array', 'items': items}, inData)


asRootDict = partial(with_object, inData=True)
asRootArray = partial(with_array, inData=True)
