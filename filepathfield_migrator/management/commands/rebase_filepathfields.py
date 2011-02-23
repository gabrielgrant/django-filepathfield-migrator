"""Fixes FilePathFields whose base paths have changed.

takes a 'base_paths' file, which comes from the dumpbase_filepathfields command

it contains a list of ('applabel.modelname.field', '/path/field/root/') tuples.
"""

import os
import sys
from django.core.management.base import CommandError, BaseCommand
try:
    from django.db import DEFAULT_DB_ALIAS
except ImportError:
    DEFAULT_DB_ALIAS = None
from optparse import make_option

from django.db.models import get_model
from django.utils import simplejson as json

class Command(BaseCommand):
    help = 'Fixes FilePathFields whose base paths have changed.'
    args = "base_path_dump"

    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a specific database to load '
                'fixtures into. Defaults to the "default" database.'),
    )

    def handle(self, base_path_dump, **options):
        using = options.get('database', DEFAULT_DB_ALIAS)
        if using:
            save_kwargs = {'using': using}
        else:
            save_kwargs = {}

        if base_path_dump == '-':
            f = sys.stdin
        else:
            f = open(base_path)
        for field, old_base in json.load(f):
            app_name, model_name, field_name = field.split('.')
            model = get_model(app_name, model_name)
            field = model._meta.get_field(field_name)
            new_base = field.path
            for obj in model.objects.exclude(**{str(field_name): ''}):
                filepath = getattr(obj, field_name)
                relpath = os.path.relpath(filepath, old_base)
                new_path = os.path.join(new_base, relpath)
                setattr(obj, field_name, new_path)
                obj.save(**save_kwargs)

