from django.test import TestCase


class DefaultTestCase(TestCase):

    def test_something_that_will_pass(self):
        self.assertFalse(False)

