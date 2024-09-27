# core/management/commands/unittest.py
from django.core.management.commands.test import Command as TestCommand

class Command(TestCommand):
    """
    自定義的 unittest 命令，默認使用自定義的 UnitTestRunner。
    """
    def execute(self, *args, **options):
        # 設定自定義的測試運行器
        test_class = 'core.runner.unit_test_runner.UnitTestRunner'  # 將此替換成你自定義的 runner 路徑
        options['testrunner'] = test_class
        super().execute(*args, **options)
