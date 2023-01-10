import random
import unittest

from quantestpy import PauliCircuit
from quantestpy.simulator.exceptions import PauliCircuitError


class TestAssertIsCorrectRegAndQubitVal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.simulator.pauli_circuit.test_assert_is_correct_reg_and_qubit_val
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        circ = PauliCircuit(100)
        register = random.sample(range(0, 100), k=20)
        qubit_value = [random.randint(0, 1) for _ in range(20)]
        self.assertIsNone(
            circ._assert_is_correct_reg_and_qubit_val(
                register=register,
                qubit_val=qubit_value
            )
        )

    def test_raise_from_nonconsistent_length(self,):
        circ = PauliCircuit(100)
        register = random.sample(range(0, 100), k=20)
        qubit_value = [random.randint(0, 1) for _ in range(19)]
        expected_error_msg = "Length of register and that of " \
            + "qubit_val must be the same."

        with self.assertRaises(PauliCircuitError) as cm:
            circ._assert_is_correct_reg_and_qubit_val(
                register=register,
                qubit_val=qubit_value
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)
