from __future__ import unicode_literals

from django.apps import AppConfig


class JsonmirrorConfig(AppConfig):
    name = 'jsonmirror'
    
    def ready(self):
        # models registration from settings
        from django.conf import settings
        from jsonmirror.register_models import register_model, get_model_from_path
        mirrored_models = getattr(settings, 'MIRRORED_MODELS', [])
        for modpath in mirrored_models:
            model = get_model_from_path(modpath)
            register_model(model)
            
