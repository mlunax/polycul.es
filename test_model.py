from unittest import TestCase

import model


class TestMe(TestCase):
    def test_me(self):
        self.assertFalse(model.Polycule is None)
