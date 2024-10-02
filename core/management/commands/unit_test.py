from django.core.management.commands.test import Command as TestCommand

class Command(TestCommand):
    def execute(self, *args, **options):
        test_class = 'core.runner.unit_test_runner.UnitTestRunner'
        options['testrunner'] = test_class
        super().execute(*args, **options)
