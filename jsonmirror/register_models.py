# -*- coding: utf-8 -*-

import importlib
from django.db.models.signals import post_save, post_delete
from jsonmirror.conf import BACKEND
if BACKEND == "rethinkdb":
    from jsonmirror.backends.rethinkdb.signals import model_save, model_delete
    
    
def register_model(model):
    post_save.connect(model_save, sender=model)
    post_delete.connect(model_delete, sender=model)
    return

def get_model_from_path(modpath):
    modsplit = modpath.split('.')
    path = '.'.join(modsplit[:-1])
    modname = '.'.join(modsplit[-1:])
    module = importlib.import_module(path)
    model = getattr(module, modname)
    return model
