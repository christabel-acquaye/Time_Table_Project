Schema
------

The ``schema`` package is where we define the request data schema for a
particular feature.

::

   .
   ├── features
   .   └── users
   .       └── schema.py

The data validation is done using `json_schema`_ with full support for
Draft 7, Draft 6, Draft 4 and Draft 3.

.. _json_schema: https://github.com/Julian/jsonschema
