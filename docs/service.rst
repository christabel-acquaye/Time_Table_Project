
Service
-------

The ``service`` package is where we define the data service handlers for
a particular feature. For example; a function to ``get_user_by_email``.

::

   .
   ├── features
   .   └── users
   .       └── service
   .           └── __init__.py
   .           └── queries.py

The ``queries.py`` is where you would specify your database query
strings and the data service handlers should be exposed in
``__init__.py``
