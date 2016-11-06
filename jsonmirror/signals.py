# -*- coding: utf-8 -*-

import json
from django.core import serializers
from jsonmirror.conf import BACKEND, DB, TABLE
if BACKEND == "rethinkdb":
    from djR.r_producers import R
    from jsonmirror.backends.rethinkdb import document_exists


def model_save_json(sender, instance, created, **kwargs):
    data = json.loads(serializers.serialize("json", [instance])[1:-1])
    if BACKEND == "rethinkdb":
        if created:
            res = R.write(DB, TABLE, data)
        else:
            # check if the document exists or not
            modelname = str(instance._meta)
            document_exists_in_db = document_exists(DB, TABLE, modelname, instance.pk)
            if not document_exists_in_db:
                res = R.write(DB, TABLE, data)
            else:
                modelname = str(instance._meta)
            # write
            res = R.update(DB, TABLE, data, modelname, instance.pk)
    return res
            
def model_delete_json(sender, instance, **kwargs):
    modelname = str(instance._meta)
    document_exists_in_db = document_exists(DB, TABLE, modelname, instance.pk)
    if document_exists_in_db:
        filters = {"model": modelname, "pk": instance.pk}
        R.delete(DB, TABLE, filters)
    return
