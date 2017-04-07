# -*- coding: utf-8 -*-

from jsonmirror.conf import get_option
from jsonmirror.conf import BACKEND, DB, TABLE
if BACKEND == "rethinkdb":
    from djR.r_producers import R
    from jsonmirror.backends.rethinkdb import document_exists


def model_save(sender, instance, created, **kwargs):
    from jsonmirror.utils import mirror_model
    mirror_model(instance, created, True)
    return


def model_delete(sender, instance, **kwargs):
    modelname = str(instance._meta)
    soft_delete = get_option(instance, "soft_delete")
    if soft_delete is False:
        document_exists_in_db = document_exists(DB, TABLE, modelname, instance.pk)
        if document_exists_in_db:
            filters = {"model": modelname, "pk": instance.pk}
            R.delete_filtered(DB, TABLE, filters)
    return
