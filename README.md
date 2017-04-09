# Django Json Mirror

Mirror and sync Django models in a json in another database. 

## Install

Clone then:

  ```python
pip install -r django-jsonmirror/requirements.txt
  ```

Add ``"jsonmirror",`` to installed apps.

## Settings

Declare the databases:

  ```python
SITE_SLUG = "my_site"
MIRROR_DATABASES = {
    "main": {
        "name": SITE_SLUG,
        "type": "sqlite"
    },
    "alt": {
        "name": SITE_SLUG,
        "type": "rethinkdb"
    }
}
  ```

The `SITE_SLUG` setting is required

## Register models

Declare the models you want to mirror in `settings.py` and set the database options for each model to mirror:

  ```python
MIRRORED_MODELS = {
    'django.contrib.auth.models.User': {
        "alt": {
           "table": "users",
           "imutable": False
        }
    },
    'myapp.models.MyModel': {
         "main": {
            "table": "mytable",
            "imutable": False,
            "soft_delete": False
        },
        "alt": {
            "table": "pages"
        }
    }
}
  ```

Note that `table` is required

### Database options

#### Imutability

Set to `True` by default: the database is write only

#### Soft delete

When imutability is turned of the `soft delete` option, enabled by default, will mark documents as deleted
  
## Backends

### [Rethinkdb](https://rethinkdb.com)

Settings:

  ```python
# required
MIRROR_DB = "mydb"
MIRROR_TABLE = "mymirrortable"

# optional:
RETHINKDB_HOST = "127.0.0.1" # default
RETHINKDB_USER = "admin" # default is None
RETHINKDB_PASSWORD = "mypassword" # default is None
  ```

### [SqlAlchemy](http://www.sqlalchemy.org/)

Settings:

  ```python
# required
MIRROR_SQL_ENGINE = 'sqlite:///mirror.db'
  ```
Refer to SqlAlchemy docs for how to [setup db urls](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)

Note: the sql backend is limited for now: it saves the data to an unique table named `mirror` with django model path and
the instance pk to use as compound index to retrieve the data.

## Models synchronization

The models declared for mirroring will be auto synchronized in the secondary databases at each save/delete 
operation performed on them

The command ``python manage.py sync_models`` will mirror all the models declared in the ``MIRRORED_MODELS`` setting.
They will be auto created/updated in the secondary databases using this command.

## Todo

- [x] SqlAlchemy backend
- [ ] Redis backend
- [ ] Support DRF serializers
- [ ] Support custom serializers
- [ ] Better handling of connection failure
 