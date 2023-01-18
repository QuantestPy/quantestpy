import unittest

from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer as CD


class TestAddObjInLineIdToText(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.quantestpy_circuit_drawer.test_add_obj_in_line_id_to_text
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.001s

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

        cd.add_obj_in_line_id_to_text(line_id=1, obj="dummy")
        actual = cd._line_id_to_text
        expect = {
            0: "a",
            1: "bdummy",
            2: "c"
        }
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = []
        self.assertEqual(actual, expect)

        actual = cd._gate_length
        expect = 0
        self.assertEqual(actual, expect)

    def test_replace_true(self):
        qc = QuantestPyCircuit(2)
        cd = CD(qc)

        cd._line_id_to_text = {
            0: "a",
            1: "b",
            2: "c"
        }

        cd.add_obj_in_line_id_to_text(line_id=1, obj="dummy", replace_obj=True)
        actual = cd._line_id_to_text
        expect = {
            0: "a",
            1: "dummy",
            2: "c"
        }
        self.assertEqual(actual, expect)

    def test_occupy_true(self):
        qc = QuantestPyCircuit(2)
        cd = CD(qc)

        cd._line_id_to_text = {
            0: "a",
            1: "b",
            2: "c"
        }

        cd.add_obj_in_line_id_to_text(
            line_id=1, obj="dummy", occupy_line_id=True)
        actual = cd._line_id_to_text
        expect = {
            0: "a",
            1: "bdummy",
            2: "c"
        }
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [1]
        self.assertEqual(actual, expect)

    def test_update_gate_length_true(self):
        qc = QuantestPyCircuit(2)
        cd = CD(qc)

        cd._line_id_to_text = {
            0: "a",
            1: "b",
            2: "c"
        }

        cd.add_obj_in_line_id_to_text(
            line_id=1, obj="dummy", update_gate_length=True)
        actual = cd._line_id_to_text
        expect = {
            0: "a",
            1: "bdummy",
            2: "c"
        }
        self.assertEqual(actual, expect)

        actual = cd._gate_length
        expect = 5
        self.assertEqual(actual, expect)
