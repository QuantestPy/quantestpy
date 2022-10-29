import unittest

from quantestpy import FastTestCircuit
from quantestpy.exceptions import QuantestPyTestCircuitError
from quantestpy.fast_test_circuit import _IMPLEMENTED_GATES


class TestFastTestCircuitAddGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_fast_test_circuit_add_gate
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        circ = FastTestCircuit(100)
        circ.add_gate(
            {"name": "x",
             "target_qubit": [3],
             "control_qubit": [0, 1],
             "control_value": [1, 1]}
        )
        circ.add_gate(
            {"name": "y",
             "target_qubit": [10, 11, 12],
             "control_qubit": [5],
             "control_value": [0]}
        )

        expected_gates = [
            {"name": "x",
             "target_qubit": [3],
             "control_qubit": [0, 1],
             "control_value": [1, 1],
             "parameter": []},
            {"name": "y",
             "target_qubit": [10, 11, 12],
             "control_qubit": [5],
             "control_value": [0],
             "parameter": []}
        ]
        actual_gates = circ._gates

        self.assertEqual(expected_gates, actual_gates)

    def test_raise_from_non_existing_gate_name(self,):
        circ = FastTestCircuit(100)
        expected_error_msg = \
            'rz gate is not implemented.\n' \
            + f'Implemented gates: {_IMPLEMENTED_GATES}'

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            circ.add_gate(
                {"name": "rz",
                 "target_qubit": [20],
                 "control_qubit": [],
                 "control_value": [],
                 "parameter": [0.1]}
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)
