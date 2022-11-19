import random
import unittest

import numpy as np

from quantestpy import PauliCircuit


class TestExecuteSwapgate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.pauli_circuit.test_execute_swap_gate
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.002s

    OK
    $
    """

    def test_qubit_value_and_phase_after_swap_operation(self,):
        circ = PauliCircuit(100)
        qubit_ids = random.sample(range(0, 100), k=50)
        circ._qubit_value[qubit_ids] = 1
        qubit_ids = random.sample(range(0, 100), k=50)
        circ._qubit_phase[qubit_ids] = np.pi/2.

        target_qubit = random.sample(range(0, 100), k=2)
        expected_qubit_value = circ._qubit_value[target_qubit]
        expected_qubit_phase = circ._qubit_phase[target_qubit]

        circ._execute_swap_gate(target_qubit)
        target_qubit.reverse()
        actual_qubit_value = circ._qubit_value[target_qubit]
        actual_qubit_phase = circ._qubit_phase[target_qubit]

        self.assertTrue(np.allclose(expected_qubit_value, actual_qubit_value))
        self.assertTrue(np.allclose(expected_qubit_phase, actual_qubit_phase))
