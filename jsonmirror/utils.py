from __future__ import print_function
import json
from django.core import serializers
from django.utils import timezone
from django.conf import settings
from jsonmirror.conf import BACKEND, TABLE, get_option
if BACKEND == "rethinkdb":
    from jsonmirror.backends.rethinkdb import mirror_model, delete_model
elif BACKEND == "sqlite":
    from jsonmirror.backends.sqlite import mirror_model, delete_model


def delete_model_s(instance):
    delete_model(instance)
    return

def mirror_model_s(instance, created=False, verbose=False):
    table = TABLE
    custom_table = get_option(instance, "table")
    if custom_table is not None:
        table = custom_table
    data = prepare_data(instance)
    res = mirror_model(instance, data, created, verbose, table)
    return res

def prepare_data(instance):
    # prepare data
    data = json.loads(serializers.serialize("json", [instance])[1:-1])
    index = get_option(instance, "index_field")
    if index is not None:
        fields_names = [f.name for f in instance._meta.get_fields()]
        if index in fields_names:
            index_value = getattr(instance, index, None)
            data["index"] = index_value
    data["timestamp"] = int(timezone.now().strftime("%s"))
    return data
