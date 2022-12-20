import unittest

from quantestpy import PauliCircuit
from quantestpy.assertion.color_ctrl_val import CircuitDrawerGateColoring


class TestIsGateExecuted(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.assertion.color_ctrl_val.test_is_gate_executed
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.003s

    OK
    $
    """

    def test_true_regular(self,):
        pc = PauliCircuit(3)
        pc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [1],
                     "control_value": []})
        gc = CircuitDrawerGateColoring(pc)

        self.assertTrue(gc.is_gate_executed(gate_id=0))

    def test_true_with_ctrl(self,):
        pc = PauliCircuit(3)
        pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
                     "control_value": [0]})
        gc = CircuitDrawerGateColoring(pc)

        self.assertTrue(gc.is_gate_executed(gate_id=0))

    def test_false_with_ctrl(self,):
        pc = PauliCircuit(3)
        pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
                     "control_value": [1]})
        gc = CircuitDrawerGateColoring(pc)

        self.assertFalse(gc.is_gate_executed(gate_id=0))
