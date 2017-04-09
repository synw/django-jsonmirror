from __future__ import print_function
import json
from django.core import serializers
from django.utils import timezone


def prepare_data(instance):
    # prepare data
    data = json.loads(serializers.serialize("json", [instance])[1:-1])
    index = get_option(instance, "index_field")
    if index is not None:
        fields_names = [f.name for f in instance._meta.get_fields()]
        if index in fields_names:
            index_value = getattr(instance, index, None)
            data["index"] = index_value
    data["timestamp"] = int(timezone.now().strftime("%s"))
    return data
