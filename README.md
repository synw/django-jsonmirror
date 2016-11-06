# Django Json Mirror

Mirror and sync Django models in a json database. 

## Install

  ```python
pip install git+https://github.com/synw/django-jsonmirror.git
  ```

Add ``"jsonmirror",`` to installed apps.

## Configure your models

Declare the models you want to mirror: in settings.py:

  ```python
MIRRORED_MODELS = ['myapp.models.MyModel', 'django.contrib.auth.models.User']
  ```
  
## Backends

Currently only [Rethinkdb](https://rethinkdb.com) is available as backend. Setup:

  ```python
pip install rethinkdb geojson jsonschema djangoajax six python-dateutil
pip install git+https://github.com/dmpayton/reqon.git
pip install git+https://github.com/synw/django-R.git
  ```

Installed apps:

  ```python
"django_ajax",
"djR",
"jsonmirror",
  ```

## Models synchronization

The command ``python manage.py sync_models`` will mirror all the models declared in the ``MIRRORED_MODELS`` setting.

All the models declared in this setting will be auto created/deleted/updated in the json database.

 