import unittest

from quantestpy.simulator.pauli_circuit import PauliCircuit
from quantestpy.visualization.pauli_circuit_drawer import \
    PauliCircuitDrawer as CD


class TestIsGateExecuted(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.pauli_circuit_drawer.test_is_gate_executed
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.003s

    OK
    $
    """

    def test_true(self,):
        pc = PauliCircuit(10)
        pc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [3],
                     "control_value": []})
        cd = CD(pc)
        self.assertTrue(cd.is_gate_executed(gate_id=0))

    def test_false(self,):
        pc = PauliCircuit(10)
        pc.add_gate({"name": "y", "control_qubit": [0], "target_qubit": [3],
                     "control_value": [1]})
        cd = CD(pc)
        self.assertFalse(cd.is_gate_executed(gate_id=0))
