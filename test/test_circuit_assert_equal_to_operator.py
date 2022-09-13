import unittest
import numpy as np

from quantestpy import TestCircuit
from quantestpy import circuit
from quantestpy.exceptions import QuantestPyAssertionError


class TestCircuitAssertEqualToOperator(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_circuit_assert_equal_to_operator
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.003s

    OK
    $
    """

    def setUp(self) -> None:
        """Prepare the Bell state"""
        self.test_circ = TestCircuit(2)
        self.test_circ.add_gate(
            {"name": "h", "target_qubit": [0], "control_qubit": [],
             "control_value": [], "parameter": []})
        self.test_circ.add_gate(
            {"name": "cx", "control_qubit": [0],  "target_qubit": [1],
             "control_value": [1], "parameter": []})

    def tearDown(self) -> None:
        del self.test_circ

    def test_assert_equal_to_operator_1(self,):

        expected_operator = np.array(
            [[1, 0, 1, 0],
             [0, 1, 0, 1],
             [0, 1, 0, -1],
             [1, 0, -1, 0]]
        )/np.sqrt(2.)

        self.assertIsNone(
            circuit.assert_equal_to_operator(
                operator_=expected_operator,
                circuit=self.test_circ
            )
        )

    def test_assert_equal_to_operator_2(self,):

        expected_operator = np.array(
            [[1, 0, 1, 0],
             [0, 1, 0, 1],
             [0, 1, 0, -1],
             [1, 0, -1, 0]]
        )/np.sqrt(2.)

        with self.assertRaises(QuantestPyAssertionError):
            circuit.assert_equal_to_operator(
                operator_=expected_operator,
                circuit=self.test_circ,
                from_right_to_left_for_qubit_ids=True  # Qiskit convention
            )

    def test_assert_equal_to_operator_3(self,):

        expected_operator = np.array(
            [[1, 1, 0, 0],
             [0, 0, 1, -1],
             [0, 0, 1, 1],
             [1, -1, 0, 0]]
        )/np.sqrt(2.)  # Qiskit convention

        self.assertIsNone(
            circuit.assert_equal_to_operator(
                operator_=expected_operator,
                circuit=self.test_circ,
                from_right_to_left_for_qubit_ids=True  # Qiskit convention
            )
        )

    def test_assert_equal_to_operator_4(self,):

        expected_operator = np.array(
            [[1, 1, 0, 0],
             [0, 0, 1, -1],
             [0, 0, 1, 1],
             [1, -1, 0, 0]]
        )/np.sqrt(2.)  # Qiskit convention

        with self.assertRaises(QuantestPyAssertionError):
            circuit.assert_equal_to_operator(
                operator_=expected_operator,
                circuit=self.test_circ
            )
