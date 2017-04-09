# -*- coding: utf-8 -*-

import importlib
from django.conf import settings


MIRRORED_MODELS = getattr(settings, 'MIRRORED_MODELS', [])
MIRROR_DATABASES = getattr(settings, 'MIRROR_DATABASES', [])

def get_model_from_path(modpath):
    modsplit = modpath.split('.')
    path = '.'.join(modsplit[:-1])
    modname = '.'.join(modsplit[-1:])
    module = importlib.import_module(path)
    model = getattr(module, modname)
    return model

def get_db(dbname):
    dbs = MIRROR_DATABASES
    db = dbs[dbname]
    return db

def get_db_options(instance):
    db_options = {}
    for mod in MIRRORED_MODELS.keys():
        model = get_model_from_path(mod)
        dbs = MIRRORED_MODELS[mod]
        if model == instance.__class__:
            for name in dbs.keys():
                db_options[name] = dbs[name]
    return db_options

def get_option(instance, db, option_name):
    for mod in MIRRORED_MODELS.keys():
        model = get_model_from_path(mod)
        dbs = MIRRORED_MODELS[mod]
        if model == instance.__class__:
            #print "OPTIONS: "+str(options.keys())+" / "+option_name
            options = dbs[db]
            if option_name in options.keys():
                return options[option_name]
    return None
