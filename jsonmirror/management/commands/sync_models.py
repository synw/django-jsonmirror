from __future__ import print_function
from django.core.management.base import BaseCommand
from jsonmirror.management.conf import bcolors
from jsonmirror.producers import mirror_model_s
from jsonmirror.conf import get_model_from_path, MIRRORED_MODELS


class Command(BaseCommand):
    help = 'Mirror models whith jsonmirror'

    def handle(self, *args, **options):
        num_models = 0
        num_instances = 0
        for modelpath in MIRRORED_MODELS.keys():
            num_models += 1
            model = get_model_from_path(modelpath)
            print("* Syncing model "+bcolors.OKBLUE+modelpath+bcolors.ENDC)
            created = 0
            updated = 0
            for instance in model.objects.all():
                num_instances += 1
                c, u = mirror_model_s(instance)
                if c is True:
                    created += 1
                if u is True:
                    updated += 1
            print(bcolors.BOLD+bcolors.BOLD+str(created)+bcolors.ENDC+" documents created")
            print(bcolors.BOLD+bcolors.BOLD+str(created)+bcolors.ENDC+" documents updated")
        print("[ "+bcolors.OKGREEN+bcolors.BOLD+"OK"+bcolors.ENDC+" ] "+bcolors.BOLD+\
              str(num_instances)+bcolors.ENDC+" instances synced in "+\
              str(num_models)+" models")
        return
