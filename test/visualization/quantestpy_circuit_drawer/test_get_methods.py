import unittest

from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer as CD


class TestGetMethods(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.quantestpy_circuit_drawer.test_get_methods
    .......
    ----------------------------------------------------------------------
    Ran 7 tests in 0.001s

    OK
    $
    """

    def test_get_line(self,):
        actual = CD.get_line(length=4)
        expect = "────"
        self.assertEqual(actual, expect)

    def test_get_cross_line(self,):
        actual = CD.get_cross_line()
        expect = "┼"
        self.assertEqual(actual, expect)

    def test_get_wire(self,):
        actual = CD.get_wire()
        expect = "│"
        self.assertEqual(actual, expect)

    def test_get_space(self,):
        actual = CD.get_space(length=4)
        expect = "    "
        self.assertEqual(actual, expect)

    def test_get_tgt(self,):
        name_lst = ["x", "y", "z", "h"]
        obj_lst = ["[X]", "[Y]", "[Z]", "[H]"]
        for name, obj in zip(name_lst, obj_lst):
            actual = CD.get_tgt(name)
            expect = obj
            self.assertEqual(actual, expect)

    def test_get_ctrl(self,):
        ctrl_val_lst = [1, 0]
        obj_lst = ["■", "o"]
        for ctrl_val, obj in zip(ctrl_val_lst, obj_lst):
            actual = CD.get_ctrl(ctrl_val)
            expect = obj
            self.assertEqual(actual, expect)

    def test_get_inter_line_id(self,):
        actual = CD.get_inter_line_id(2, 6)
        expect = [3, 4, 5]
        self.assertEqual(actual, expect)
