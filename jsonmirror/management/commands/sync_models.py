# -*- coding: utf-8 -*-

import json
from django.core import serializers
from django.core.management.base import BaseCommand
from django.conf import settings
from jsonmirror.management.conf import bcolors
from jsonmirror.conf import BACKEND, DB, TABLE
from jsonmirror.register_models import get_model_from_path
if BACKEND == "rethinkdb":
    import rethinkdb as r
    from djR.r_producers import R
    from jsonmirror.backends.rethinkdb import document_exists


class Command(BaseCommand):
    help = 'Mirror models into '+BACKEND

    def handle(self, *args, **options):
        endres = {"updated":0, "created":0, "num_models":0}
        conn = R.connect()
        if BACKEND == "rethinkdb":
            mirrored_models = getattr(settings, 'MIRRORED_MODELS', [])
            for modpath in mirrored_models:
                model = get_model_from_path(modpath)
                modelname = str(model._meta)
                print "* Syncing model "+bcolors.OKBLUE+modelname+bcolors.ENDC
                instances = model.objects.all()
                for instance in instances:
                    data = json.loads(serializers.serialize("json", [instance])[1:-1])
                    if document_exists(DB, TABLE, modelname, instance.pk) is True:
                        r.db(DB).table(TABLE).filter((r.row['model'] == modelname) & (r.row['pk'] == instance.pk)).update(data, return_changes=False).run(conn)
                        print "[ "+modelname+" ] Document "+str(instance.pk)+" updated"
                        endres["updated"] = endres["updated"]+1
                    else:
                        r.db(DB).table(TABLE).insert(data, return_changes=False).run(conn)
                        print "[ "+modelname+" ] Document "+str(instance.pk)+" created"
                        endres["created"] = endres["created"]+1
                endres["num_models"] += 1
        conn.close()
        print "[ "+bcolors.OKGREEN+bcolors.BOLD+"OK"+bcolors.ENDC+" ] "+bcolors.BOLD+str(endres["num_models"])+bcolors.ENDC+" models synced"
        print str(endres["created"])+" documents created"
        print str(endres["updated"])+" documents updated"
        return
