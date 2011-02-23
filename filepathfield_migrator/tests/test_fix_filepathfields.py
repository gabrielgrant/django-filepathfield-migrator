import sys
import os
from StringIO import StringIO
from django.test import TestCase
from django.core.management import call_command
from filepathfield_migrator.tests.models import Page

class FixFilePathFieldTests(TestCase):
    def setUp(self):
        self.real_stdout = sys.stdout
        sys.stdout = StringIO()
        self.real_stdin = sys.stdin
        sys.stdin = StringIO()

    def tearDown(self):
        sys.stdout = self.real_stdout
        sys.stdin = self.real_stdin

    def test_full_fix(self):
        template_field = Page._meta.get_field('template')
        p = Page(template='/tmp/test.html')  # set it to a wrong value
        p.save()
        right_path = os.path.join(template_field.path, 'test.html')
        call_command('dumpbase_filepathfields', 'tests')
        sys.stdin.write(sys.stdout.getvalue().replace(template_field.path, '/tmp'))
        sys.stdin.seek(0)
        call_command('rebase_filepathfields', '-')
        self.assertEqual(right_path, Page.objects.get().template)
