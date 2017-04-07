from __future__ import print_function
import json
from django.core import serializers
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from django.conf import settings
from jsonmirror.conf import BACKEND, TABLE, get_option
if BACKEND == "rethinkdb":
    from jsonmirror.backends.rethinkdb.signals import model_save, model_delete
    from jsonmirror.backends.rethinkdb import mirror_model as r_mirror_model


def register_model(model):
    post_save.connect(model_save, sender = model)
    post_delete.connect(model_delete, sender = model)
    return

def prepare_data(instance):
    # prepare data
    data = json.loads(serializers.serialize("json", [instance])[1:-1])
    index = get_option(instance, "index_field")
    if index is not None:
        fields_names = [f.name for f in instance._meta.get_fields()]
        if index in fields_names:
            index_value = getattr(instance, index, None)
            data["index"] = index_value
            #print json.dumps(data, indent = 4)
        #else:
        #    print("No field named "+index)
    data["timestamp"] = int(timezone.now().strftime("%s"))
    return data

def mirror_model(instance, created=False, verbose=False):
    table = TABLE
    custom_table = get_option(instance, "table")
    if custom_table is not None:
        table = custom_table
    data = prepare_data(instance)
    if BACKEND == "rethinkdb":
        res = r_mirror_model(instance, data, created, verbose, table)
    return res
