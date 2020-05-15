from .utilities import with_key


class BaseError(Exception):
    """Base exception for all the custom API errors

    Arguments:
        Exception {Exception} -- exception

    Returns:
        Dict -- jsonified error format
    """

    def __init__(self, message=None, status_code=400, payload=None):
        super(BaseError, self).__init__(message)
        self.status_code = status_code
        self.payload = payload
        self.message = message

    def to_dict(self):
        """
        Get a dictionary representation of this error instance
        """
        return format_error(self.message, self.status_code, self.payload)


def format_error(message: str, status_code: int, data=None):
    """format error

    Arguments:
        message {str} -- error message
        status_code {int} -- status code

    Keyword Arguments:
        data {Union[Dict, None]} -- extra error guide (default: {None})

    Returns:
        Dict -- jsonified error
    """
    return {'error': {**with_key(data=data, message=message)}, **with_key(statusCode=status_code)}


HTTP_404_ERROR = BaseError('Requested url not found', 404)
HTTP_503_ERROR = BaseError('Service Unavailable', 503)
HTTP_405_ERROR = BaseError('Method not allowed', 405)
HTTP_500_ERROR = BaseError(
    'Something went wrong, our team will investigate into this', 500)

AUTHENICATION_ERROR = BaseError('Authentication Failed', 401)
PERMISSION_DENIED = BaseError('Permission Denied', 401)


def JSON_VALIDATION_ERROR(data):
    return BaseError('Invalid json data', 442, data)


def QUERY_NOT_FOUND(query_type):
    return RuntimeError(f'Unknown query; {query_type}')


class NotEnoughRooms(Exception):
    def __init__(self, message='No rooms available to allocate students'):
        # Call the base class constructor with the parameters it needs
        super(NotEnoughRooms, self).__init__(message)
