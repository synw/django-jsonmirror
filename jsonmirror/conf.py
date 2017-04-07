# -*- coding: utf-8 -*-

import importlib
from django.conf import settings


MIRRORED_MODELS = getattr(settings, 'MIRRORED_MODELS', [])

BACKEND = getattr(settings, 'MIRROR_BACKEND', "rethinkdb")

DB = getattr(settings, 'MIRROR_DB')
TABLE = getattr(settings, 'MIRROR_TABLE')

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
