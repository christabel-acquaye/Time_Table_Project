# Documentation

This is the documentation for {{Project}}, a {{description}}. This project requires python >= 3.8 

## Project Structure

Please find a documentation of the project structure [here](./docs/folder-structure.rst).

## API

## Setting up Project
- Run the command below to install the project dependencies,

    ```
    make install
    ```
- Copy `.env.example` and rename to `.env`.
- Configure the environment variables in the `.env`.
- Run the command to start the server
    ```
    make run
    ```

## Packages

Here are a list of all the packages and modules included.

- [Flask](https://pypi.org/project/Flask/): Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.

- [MySQL-python](https://pypi.org/project/MySQL-python/): MySQLdb is an interface to the popular MySQL database server for Python.

- [python-dotenv](https://pypi.org/project/python-dotenv/): Reads the key-value pair from .env file and adds them to environment variable. It is great for managing app settings during development and in production using [12-factor principles](https://12factor.net/).

- [Jsonschema](https://pypi.org/project/jsonschema/): jsonschema is an implementation of [JSON Schema](https://json-schema.org/) for Python (supporting 2.7+ including Python 3).

- [Gunicorn](https://pypi.org/project/gunicorn/): Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for UNIX. It’s a pre-fork worker model ported from Ruby’s Unicorn project.

- [Pycodestyle](https://pypi.org/project/pycodestyle/): pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.

- [Gitchangelog](https://pypi.org/project/gitchangelog/): Use your commit log to make beautifull and configurable changelog file.

## Authors

- [Benjamin Arko Afrasah](https://github.com/Silvrash)
