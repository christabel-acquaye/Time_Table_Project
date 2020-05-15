import os
from functools import reduce
from uuid import uuid4
import hashlib
import binascii
import os


def get_env(key: str, default=None):
    """ get value from environment """
    return os.getenv(key) or default


def with_key(**kwargs):
    """ spread arguments to key - value pairs """
    return {k: v for k, v in kwargs.items()}


def uuid():
    return uuid4().__str__()


def get_template_path(name: str):
    """ get path to template file """
    return os.path.join(__file__, '../templates', name)


def compose(*fs):
    def inner(f, g):
        return lambda *a, **kw: f(g(*a, **kw))

    return reduce(inner, fs)


def hash_value(string: str):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(80)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512',
        string.encode('utf-8'),
        salt,
        100000
    )
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_hash(hashed_string: str, string: str):
    """Verify a stored password against one provided by user"""
    salt = hashed_string[:64]
    hashed_string = hashed_string[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512',
        string.encode('utf-8'),
        salt.encode('ascii'),
        100000
    )
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == hashed_string
