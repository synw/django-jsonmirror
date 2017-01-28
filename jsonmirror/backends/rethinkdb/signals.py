# -*- coding: utf-8 -*-

from jsonmirror.conf import BACKEND, DB, TABLE
if BACKEND == "rethinkdb":
    from djR.r_producers import R
    from jsonmirror.backends.rethinkdb import document_exists


def model_save(sender, instance, created, **kwargs):
    from jsonmirror.utils import mirror_model
    res = mirror_model(instance, created, True)
    #print str(res)
    return


def model_delete(sender, instance, **kwargs):
    modelname = str(instance._meta)
    document_exists_in_db = document_exists(DB, TABLE, modelname, instance.pk)
    if document_exists_in_db:
        filters = {"model": modelname, "pk": instance.pk}
        R.delete(DB, TABLE, filters)
    return
