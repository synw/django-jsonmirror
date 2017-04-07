# -*- coding: utf-8 -*-

from jsonmirror.utils import mirror_model_s, delete_model_s


def model_save(sender, instance, created, **kwargs):
    mirror_model_s(instance, created, True)
    return


def model_delete(sender, instance, **kwargs):
    delete_model_s(instance)
    return
