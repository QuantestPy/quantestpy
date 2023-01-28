import unittest

from quantestpy.assertion.assert_unary_iteration import _is_a_in_b


class TestIsAinB(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.assertion.assert_unary_iteration.test_is_a_in_b
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s
    OK
    $
    """

    def test_return_true(self):
        a = [1, 2, 3, 4]
        b = [4, 1, 5, 6, "i"]
        self.assertTrue(_is_a_in_b(a, b))

    def test_return_false(self):
        a = [1, 2, 3, 4, "j"]
        b = [10, 9, 5, 6, "i"]
        self.assertFalse(_is_a_in_b(a, b))
