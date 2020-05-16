from _shared.db_service import end_db_connection
from flask import Flask


def add_middlewares(app: Flask):
    """handler to register application middlewares

    Arguments:
            app {Flask} -- Flask App
    """
    app.teardown_appcontext(end_db_connection)
