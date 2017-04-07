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

If you want a secondary index set on your model declare the index field:

  ```python
MIRRORED_MODELS = [
    ['django.contrib.auth.models.User', {"index_field": "username"}]
]
  ```
  
If you want to record a model in a different table than the default one:

  ```python
MIRRORED_MODELS = [
    ['django.contrib.auth.models.User', {"index_field": "username", "table": "users"}]
]
  ```
  
A model is imutable by default in the destination database: it will not be updated but produces a new write. To
disable this behavior and update the data use this:

  ```python
MIRRORED_MODELS = [
    ['django.contrib.auth.models.User', {"table": "users", "imutable": False}]
]
  ```
  
All the models use soft delete: the data is not deleted from the destination database. To
disable this behavior and delete the data use this:
  
  ```python
MIRRORED_MODELS = [
    ['django.contrib.auth.models.User', {"table": "users", "soft_delete": False}]
]
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

 