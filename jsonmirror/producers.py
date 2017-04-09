from __future__ import print_function
import json
from django.core import serializers
from django.utils import timezone
from django.conf import settings
from jsonmirror.conf import get_db_options, get_db
from jsonmirror.backends.rethinkdb import mirror_model as r_mirror_model, delete_model as r_delete_model
from jsonmirror.backends.sqlite import mirror_model, delete_model


def delete_model_s(instance):
    dboptions = get_db_options(instance)
    for db in dboptions.keys():
        options = dboptions[db]
        opts = options.keys()
        imutable = True
        if "imutable" in opts:
            imutable = options["imutable"]
        soft_delete = True
        if "soft_delete" in opts:
            soft_delete = options["soft_delete"]
        table = options["table"]
        # get db
        dbobj = get_db(db)
        dbname = dbobj["name"]
        dbtype = dbobj["type"]
        if dbtype == "sqlite":
            delete_model(instance, dbname, table, imutable, soft_delete)
        elif dbtype == "rethinkdb":
            r_delete_model(instance, dbname, table, imutable, soft_delete)
    return

def mirror_model_s(instance, created=False, verbose=False):
    # get options
    dboptions = get_db_options(instance)
    for db in dboptions.keys():
        options = dboptions[db]
        table = options["table"]
        opts = options.keys()
        imutable = True
        if "imutable" in opts:
            imutable = options["imutable"]
        # get db
        db = get_db(db)
        dbname = db["name"]
        dbtype = db["type"]
        data = serialize(instance)
        if dbtype == "sqlite":
            mirror_model(instance, data, dbname, table, created, imutable)
        elif dbtype == "rethinkdb":
            r_mirror_model(instance, data, dbname, table, created, imutable)
    return

def serialize(instance):
    # prepare data
    data = json.loads(serializers.serialize("json", [instance])[1:-1])
    """
    index = get_option(instance, "index_field")
    if index is not None:
        fields_names = [f.name for f in instance._meta.get_fields()]
        if index in fields_names:
            index_value = getattr(instance, index, None)
            data["index"] = index_value
    """
    data["timestamp"] = int(timezone.now().strftime("%s"))
    return data
