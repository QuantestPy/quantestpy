import random
import unittest

from quantestpy import PauliCircuit
from quantestpy.simulator.exceptions import PauliCircuitError


class TestAssertIsCorrectReg(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m \
        unittest test.simulator.pauli_circuit.test_assert_is_correct_reg
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.002s

    OK
    $
    """

    def test_regular(self,):
        circ = PauliCircuit(100)
        register = random.sample(range(0, 100), k=20)
        self.assertIsNone(
            circ._assert_is_correct_reg(register=register)
        )

    def test_raise_from_register_incorrect_type(self,):
        circ = PauliCircuit(100)
        register = {0, 1, 2}
        expected_error_msg = "register must be a list."

        with self.assertRaises(PauliCircuitError) as cm:
            circ._assert_is_correct_reg(register=register)

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_id_incorrect_type(self,):
        circ = PauliCircuit(100)
        register = [10.]
        expected_error_msg = "Indices in register must be integer type."

        with self.assertRaises(PauliCircuitError) as cm:
            circ._assert_is_correct_reg(register=register)

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_id_out_of_range(self,):
        circ = PauliCircuit(100)
        register = [99, 100]
        expected_error_msg = "Qubit index 100 in register is out of range."

        with self.assertRaises(PauliCircuitError) as cm:
            circ._assert_is_correct_reg(register=register)

        self.assertEqual(cm.exception.args[0], expected_error_msg)
