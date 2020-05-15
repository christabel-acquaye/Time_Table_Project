Routes
------

The ``routes`` package is a recommendation of where you can put your
route controllers for a feature.

::

   .
   ├── features
   .   └── users
   .       └── routes.py

The route controllers should be exposed in
``features/users/__init__.py`` where the would automatically be picked
and registered in the application routing configuration; ``urls.py``.

For example; in ``__init__.py`` you would expose the routes like this.

.. code:: python

   expose = [add_user, get_user, update_user, delete_user]

