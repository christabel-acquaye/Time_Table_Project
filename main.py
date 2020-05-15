from flask import Flask

from _shared import (Constants, add_middlewares, configure_app,
                     register_error_handlers)
from urls import register_urls

app = Flask(__name__)
app = configure_app(app)

register_error_handlers(app)
register_urls(app)
add_middlewares(app)

if __name__ == "__main__":
    app.run(port=Constants.PORT, debug=Constants.IS_DEV)
