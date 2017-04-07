from __future__ import unicode_literals

from django.apps import AppConfig


class JsonmirrorConfig(AppConfig):
    name = 'jsonmirror'

    def ready(self):
        # models registration from settings
        from django.conf import settings
        from jsonmirror.signals import model_save, model_delete
        from django.db.models.signals import post_save, post_delete
        
        def register_model(model):
            post_save.connect(model_save, sender = model)
            post_delete.connect(model_delete, sender = model)
            return
        
        from jsonmirror.conf import get_model_from_conf
        mirrored_models = getattr(settings, 'MIRRORED_MODELS', [])
        for modconf in mirrored_models:
            model, options = get_model_from_conf(modconf)
            register_model(model)
