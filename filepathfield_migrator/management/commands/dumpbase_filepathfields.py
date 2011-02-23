""" Dumps a list of ('applabel.modelname.field', '/path/field/root/') tuples
    for models in the given apps. This output can be used with
    rebase_filepathfields to fix FilePathFields whose base locations have
    changed (often as the result of migrating data to another environment)
    
    see http://code.djangoproject.com/ticket/6896
"""

from django.db.models import FilePathField
from django.core.management.base import BaseCommand
from django.utils import simplejson as json

class Command(BaseCommand):
    help = "Outputs information needed to fix FilePathFields"
    args = "[appname ...]"
    
    def handle(self, *app_labels, **options):
        models = get_models(app_labels)
        dumplist = []
        for model in models:
            meta = model._meta
            fields = [f for f in meta.fields if isinstance(f, FilePathField)]
            for field in fields:
                k = '.'.join([meta.app_label, meta.module_name, field.name])
                v = field.path
                dumplist.append((k, v))
        print json.dumps(dumplist)

def get_models(app_labels):
    """ Gets a list of models for the given app labels.

        Modified from dumpscript.py
    """

    from django.db.models import get_app, get_apps, get_model
    from django.db.models import get_models as get_all_models

    models = []

    # If no app labels are given, return all
    if not app_labels:
        for app in get_apps():
            models.extend(get_all_models(app))

    # Get all relevant apps
    for app_label in app_labels:
        # If a specific model is mentioned, get only that model
        if "." in app_label:
            app_label, model_name = app_label.split(".", 1)
            models.append(get_model(app_label, model_name))
        # Get all models for a given app
        else:
            models.extend(get_all_models(get_app(app_label)))

    return models
