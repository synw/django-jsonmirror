# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from jsonmirror.management.conf import bcolors
from jsonmirror.conf import BACKEND
from jsonmirror.utils import get_model_from_conf, mirror_model


class Command(BaseCommand):
    help = 'Mirror models into '+BACKEND

    def handle(self, *args, **options):
        if BACKEND == "rethinkdb":
            num_instances = 0
            num_models = 0
            mirrored_models = getattr(settings, 'MIRRORED_MODELS', [])
            for modconf in mirrored_models:
                model, options = get_model_from_conf(modconf)
                modelname = str(model._meta)
                print "* Syncing model "+bcolors.OKBLUE+modelname+bcolors.ENDC
                instances = model.objects.all()
                created = 0
                updated = 0
                for instance in instances:
                    res = mirror_model(instance)
                    if res["created"] == 1:
                        created += 1
                    if res["updated"] == 1:
                        updated += 1
                    num_instances += 1
                num_models += 1
                print str(created)+" documents created"
                print str(updated)+" documents updated"
        print "[ "+bcolors.OKGREEN+bcolors.BOLD+"OK"+bcolors.ENDC+" ] "+bcolors.BOLD+str(num_instances)+bcolors.ENDC+" instances synced in "+\
        str(num_models)+" models"
        return
