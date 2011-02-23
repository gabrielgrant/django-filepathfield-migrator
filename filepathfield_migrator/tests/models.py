import os
from django.db import models

class Page(models.Model):
    this_dir = os.path.dirname(__file__)
    template_dir = os.path.join(this_dir, 'templates')
    template = models.FilePathField(path=template_dir, match='.*\.html$', blank=False)
