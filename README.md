# Django Json Mirror

Mirror and sync Django models in a json database. 

## Install

  ```python
pip install git+https://github.com/synw/django-jsonmirror.git
  ```

Add ``"jsonmirror",`` to installed apps.

## Register models

Declare the models you want to mirror in settings.py:

  ```python
MIRRORED_MODELS = ['myapp.models.MyModel', 'django.contrib.auth.models.User']
  ```
  
## Backends

Currently only [Rethinkdb](https://rethinkdb.com) is available as backend.


### Rethinkdb

Install [django-R](https://github.com/synw/django-R).

Extra settings:

  ```python

# required
MIRROR_DB = "mydb"
MIRROR_TABLE = "mymirrortable"

# optional:
RETHINKDB_HOST = "127.0.0.1" # default
RETHINKDB_USER = "admin" # default is None
RETHINKDB_PASSWORD = "mypassword" # default is None
  ```

### Custom backend

To write your own backend you can use the setting ``MIRROR_BACKEND = "backendname_here"`` (if you do so please make some PR).

## Models synchronization

The command ``python manage.py sync_models`` will mirror all the models declared in the ``MIRRORED_MODELS`` setting.

All the models declared in this setting will be auto created/deleted/updated in the json database.

 