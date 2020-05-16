from functools import wraps
from typing import Callable, List, Union

import MySQLdb
from MySQLdb import Connection  # pylint: disable=no-name-in-module
from MySQLdb._mysql import escape_string
from MySQLdb.cursors import Cursor, DictCursor

import _shared.constants as CONSTANTS
from flask import g
from flask.logging import logging as logger

CONNECTION_PARAMS = {
    'host': CONSTANTS.DB_HOST,
    'user': CONSTANTS.DB_USER,
    'passwd': CONSTANTS.DB_PASS,
    'db': CONSTANTS.DB_NAME,
    'port': CONSTANTS.DB_PORT,
}

if not CONSTANTS.IS_DEV and CONSTANTS.SOCKET_PATH:
    CONNECTION_PARAMS['unix_socket'] = CONSTANTS.SOCKET_PATH


def get_db_connection() -> Connection:
    """get a connection from the pool

    Returns:
        Connection -- database connection
    """
    conn = None
    try:
        conn = getattr(g, 'db_connection')
    except AttributeError:
        conn = MySQLdb.connect(**CONNECTION_PARAMS)
    finally:
        setattr(g, 'db_connection', conn)
    return conn


def end_db_connection(_=None):
    """end mysql database connection
    """
    try:

        conn: Connection = getattr(g, 'db_connection')
        conn.close()
        logger.debug('Database connection closed')
    except AttributeError:
        logger.debug('Database connection does not exist')


def with_escape(func):
    """
    In order to avoid SQL Injection attacks,
    you should always escape any user provided data
    before using it inside a SQL query.
    """

    @wraps(func)
    def wrapper(**kwargs):
        if 'params' in kwargs:
            kwargs['params'] = {k: escape_string(v).decode('utf-8`') if isinstance(
                v, str) else v for k, v in kwargs['params'].items()}
        return func(**kwargs)

    return wrapper


def in_query(query_func):
    """wrap function to a database connection

    Arguments:
        query_func {Callable} -- function returning query string

    Returns:
        Callable -- wrapped function
    """
    @wraps(query_func)
    @with_escape
    def wrapper(*args, **kwargs):
        conn = get_db_connection()
        cur = get_cursor(conn)
        # prepared_query = query_func(*args, **kwargs) % kwargs.get('params')
        return run_prepared_query(cur,  prepared_query=query_func(*args, **kwargs), params=kwargs.get('params'))

    return wrapper


def run_in_transaction(func: Callable):
    """higher order function
    takes in a function and
    returns a function that executes the passed in function
    within a transaction should probably be called wrapped
    in a try catch as it does not handle
    any errors, other than rolling back the transaction

    Arguments:
        func {Callable} -- wrapped function

    Raises:
        e: Mysql error

    Returns:
        Callable -- Wrapped function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = get_db_connection()
        conn.begin()  # start transaction
        logger.debug('[SQL] BEGIN')
        try:
            results = func(*args, **kwargs)
            conn.commit()
            logger.debug('[SQL] COMMIT')
            return results
        except Exception as e:
            rollback(conn)
            logger.debug('[SQL] ROLLBACK')
            raise e

    return wrapper


def rollback(conn: Connection = None):
    """rollback database transaction

    Keyword Arguments:
        conn {Connection} -- database connection (default: {None})
    """
    conn = conn or get_db_connection()
    if conn:
        conn.rollback()
        logger.debug('ROLLBACK')


@run_in_transaction
def run_prepared_query(cur: Cursor, prepared_query: str, params=None, dim: Union['single', 'multi'] = 'single'):
    """
    Executes a database query and returns results of the data
    USE ONLY FOR, CREATE, UPDATE, DELETE,

    !!!!!  DO NOT USE FOR READ !!!!!!
    prepared query shd look like this:
    'INSERT INTO movies (title, rating) VALUES (?, ?)'
    Array should look like this:
    [['Taxi Driver', 100], ['Taxi Driver', 100]]

    Arguments:
        cur {Cursor} -- MySQLdb cursor object
        prepared_query {str} -- query string

    Keyword Arguments:
        params {Union[List, None]} -- query parameters (default: {None})
        dim {Union[single, multi]} -- single row or multiple rows (default: {'single'})

    Returns:
        List -- database results
    """

    if params is None:
        params = []

    if dim == 'multi':
        cur.executemany(prepared_query, params)
    else:
        cur.execute(prepared_query, params)

    logger.debug(f'[SQL] {cur._last_executed.decode("utf-8")}')

    return cur.fetchall()


def get_cursor(conn: Connection) -> Cursor:
    """get database cursor

    Arguments:
        conn {Connection} -- database connection

    Returns:
        Cursor -- database cursor
    """
    return conn.cursor(DictCursor)


def get_last_id(cur: Cursor) -> int:
    """get last inserted id

    Arguments:
        cur {Cursor} -- database cursor object

    Returns:
        int -- last id from insert
    """
    return cur.lastrowid


def get_last_ids(cur: Cursor) -> List[int]:
    """get last inserted ids

    Arguments:
        cur {Cursor} -- database cursor object

    Returns:
        List[int] -- last ids from insert
    """
    return [get_last_id(cur) + row for row in range(cur.rowcount)]
