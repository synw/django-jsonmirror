# -*- coding: utf-8 -*-

import importlib
import json
from django.core import serializers
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from django.conf import settings
from jsonmirror.conf import BACKEND
if BACKEND == "rethinkdb":
    from jsonmirror.backends.rethinkdb.signals import model_save, model_delete
    from jsonmirror.backends.rethinkdb import mirror_model as r_mirror_model


def register_model(model):
    post_save.connect(model_save, sender = model)
    post_delete.connect(model_delete, sender = model)
    return


def get_model_from_path(modpath):
    modsplit = modpath.split('.')
    path = '.'.join(modsplit[:-1])
    modname = '.'.join(modsplit[-1:])
    module = importlib.import_module(path)
    model = getattr(module, modname)
    return model


def get_model_from_conf(modconf):
    options = None
    if type(modconf) is str:
        model = get_model_from_path(modconf)
    elif type(modconf) is list:
        model = get_model_from_path(modconf[0])
        options = modconf[1]
    return model, options


def get_option(instance, option_name):
    mirrored_models = getattr(settings, 'MIRRORED_MODELS', [])
    for modconf in mirrored_models:    
        if type(modconf) is list:
            model, options = get_model_from_conf(modconf)
            if model == instance.__class__:
                #print "OPTIONS: "+str(options.keys())+" / "+option_name
                if option_name in options.keys():
                    return options[option_name]
    return None


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
        else:
            print "No field named "+index
    data["timestamp"] = int(timezone.now().strftime("%s"))
    return data


def mirror_model(instance, created=False, verbose=False):
    data = prepare_data(instance)
    if BACKEND == "rethinkdb":
        res = r_mirror_model(instance, data, created, verbose)
    return res
