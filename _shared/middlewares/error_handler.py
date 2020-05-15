import traceback

from flask import Flask, jsonify
from flask.logging import logging as logger

from _shared.error_service import (HTTP_404_ERROR, HTTP_405_ERROR,
                                   HTTP_500_ERROR, HTTP_503_ERROR, BaseError)


def with_error(err_type: BaseError, static=True):
    """api error handler wrapper

    Arguments:
            err_type {BaseError} -- error exception class

    Keyword Arguments:
            static {bool} -- is already initialized or thrown during (default: {True})

    Returns:
            Callable -- wrapper function to handle the error
    """

    def error_response(error):
        error = error if not static else err_type
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        logger.error(traceback.format_exc())
        return response

    return error_response


handleError = with_error(BaseError, False)
handle404Error = with_error(HTTP_404_ERROR)
handle503Error = with_error(HTTP_503_ERROR)
handle500Error = with_error(HTTP_500_ERROR)
handle405Error = with_error(HTTP_405_ERROR)


def register_error_handlers(app: Flask):
    """register error handlers for the application

    Arguments:
            app {Flask} -- Flask App
    """
    handlers = (
        (handleError, BaseError),
        (handle404Error, 404),
        (handle500Error, 500),
        (handle500Error, Exception),
        (handle503Error, 503),
        (handle405Error, 405)
    )

    for func, arg in handlers:
        app.errorhandler(arg)(func)
