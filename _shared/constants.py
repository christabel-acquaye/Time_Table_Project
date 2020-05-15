# noinspection PyPackageRequirements
from dotenv import load_dotenv

from .utilities import get_env

load_dotenv()

MODE = get_env('ENV', 'development')
IS_DEV = get_env('ENV') != 'production'
MAX_CONTENT_LENGTH = get_env('MAX_CONTENT_LENGTH')
SECRET_KEY = get_env('SECRET_KEY')
PORT = get_env('PORT')

# Exceptions are re-raised rather than being handled
# by the app’s error handlers. If not set,
# this is implicitly true if TESTING or DEBUG is enabled.
PROPAGATE_EXCEPTIONS = get_env('PROPAGATE_EXCEPTIONS', True)

DB_HOST = get_env('DB_HOST')
DB_USER = get_env('DB_USER')
DB_PASS = get_env('DB_PASS')
DB_NAME = get_env('DB_NAME')
DB_PORT = get_env('DB_PORT', 3306)
SOCKET_PATH = get_env('SOCKET_PATH')
