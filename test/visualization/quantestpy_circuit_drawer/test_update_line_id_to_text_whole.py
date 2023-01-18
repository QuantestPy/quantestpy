import unittest

from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer as CD


class TestUpdateLineIdToTextWhole(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.quantestpy_circuit_drawer.test_update_line_id_to_text_whole
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    $
    """

    def test_default(self):
        qc = QuantestPyCircuit(2)
        cd = CD(qc)

        cd._line_id_to_text = {
            0: "a",
            1: "b",
            2: "c"
        }
        cd._line_id_to_text_whole = {
            0: "x",
            1: "y",
            2: "z"
        }
        cd.update_line_id_to_text_whole()
        actual = cd.line_id_to_text_whole
        expect = {
            0: "xa",
            1: "yb",
            2: "zc"
        }
        self.assertEqual(actual, expect)

        actual = cd._line_id_to_text
        expect = {
            0: "",
            1: "",
            2: ""
        }
        self.assertEqual(actual, expect)

    def test_reset_false(self):
        qc = QuantestPyCircuit(2)
        cd = CD(qc)

        cd._line_id_to_text = {
            0: "a",
            1: "b",
            2: "c"
        }
        cd._line_id_to_text_whole = {
            0: "x",
            1: "y",
            2: "z"
        }
        cd.update_line_id_to_text_whole(reset=False)
        actual = cd.line_id_to_text_whole
        expect = {
            0: "xa",
            1: "yb",
            2: "zc"
        }
        self.assertEqual(actual, expect)

        actual = cd._line_id_to_text
        expect = {
            0: "a",
            1: "b",
            2: "c"
        }
        self.assertEqual(actual, expect)
