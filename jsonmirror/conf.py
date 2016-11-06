# -*- coding: utf-8 -*-

from django.conf import settings


MIRRORED_MODELS = getattr(settings, 'MIRRORED_MODELS', [])

BACKEND = getattr(settings, 'MIRROR_BACKEND', "rethinkdb")

DB = getattr(settings, 'MIRROR_DB')
TABLE = getattr(settings, 'MIRROR_TABLE')