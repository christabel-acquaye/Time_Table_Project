Folder Structure
================

The first step to creating an awesome application is knowing where
things are. Organisation is key to help new teammates to quickly catch
up to a code base.

Minimum Folder Structure
------------------------

All application features must be put inside ``features/`` folder as a
package. This will help keeping track of application features as the
project grows. It becomes easier to debug and understand a feature from
its folder-space.

::

   .
   ├── features
   .   └── package
   ├── _shared
   .   └── package
   ├── docs
   ├── templates
   ├── .env.example
   ├── .env
   ├── Makefile
   ├── main.py
   ├── setup.cfg
   ├── urls.py
   ├── requirements.txt
   └── templates

The ``templates/`` folder is where you put all html templates. This
folder will be automatically checked every time a template is rendered
in your routes.

   Note: The ``main.py`` is the application entry point.


.. include:: ./models.rst
.. include:: ./routes.rst
.. include:: ./schema.rst
.. include:: ./service.rst
.. include:: ./config.rst
.. include:: ./commands.rst






