from __future__ import unicode_literals

from django.apps import AppConfig


class JsonmirrorConfig(AppConfig):
    name = 'jsonmirror'

    def ready(self):
        # models registration from settings
        from django.conf import settings
        from jsonmirror.utils import register_model
        from jsonmirror.conf import get_model_from_conf
        mirrored_models = getattr(settings, 'MIRRORED_MODELS', [])
        for modconf in mirrored_models:
            model, options = get_model_from_conf(modconf)
            register_model(model)
