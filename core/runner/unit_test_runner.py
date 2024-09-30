from django.test.runner import DiscoverRunner
from django.test import SimpleTestCase
from unittest import TestSuite

class UnitTestRunner(DiscoverRunner):
    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        """
        Build a test suite that only includes tests inheriting from SimpleTestCase.
        """
        suite = super().build_suite(test_labels, extra_tests, **kwargs)
        filtered_tests = []

        for test in suite:
            if hasattr(test, '__class__'):
                test_class = test.__class__
                if issubclass(test_class, SimpleTestCase):
                    filtered_tests.append(test)

        return TestSuite(filtered_tests)

    def setup_databases(self, **kwargs):
        """Skip database setup since we are only running SimpleTestCase tests."""
        pass

    def teardown_databases(self, old_config, **kwargs):
        """Skip database teardown since we are only running SimpleTestCase tests."""
        pass
