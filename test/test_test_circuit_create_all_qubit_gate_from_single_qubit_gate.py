import unittest
import numpy as np

from quantestpy import TestCircuit
from quantestpy import test_circuit


class TestTestCircuitCreateAllQubitGateFromSingleQubitGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.test_test_circuit_create_all_qubit_gate_from_single_qubit_gate
    ........
    ----------------------------------------------------------------------
    Ran 8 tests in 0.009s

    OK
    $
    """

    def test__create_all_qubit_gate_from_single_qubit_gate_1(self,):
        h = test_circuit._H
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_single_qubit_gate(
            single_qubit_gate=h, target=0
        )

        expected_gate = np.array([[1, 0, 1, 0],
                                  [0, 1, 0, 1],
                                  [1, 0, -1, 0],
                                  [0, 1, 0, -1]]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test__create_all_qubit_gate_from_single_qubit_gate_2(self,):
        h = test_circuit._H
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_single_qubit_gate(
            single_qubit_gate=h, target=1
        )

        expected_gate = np.array([[1, 1, 0, 0],
                                  [1, -1, 0, 0],
                                  [0, 0, 1, 1],
                                  [0, 0, 1, -1]]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))
