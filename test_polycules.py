from unittest import TestCase

import polycules


class TestMe(TestCase):
    def test_me(self):
        self.assertFalse(polycules.app is None)
