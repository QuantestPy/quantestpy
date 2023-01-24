import unittest

import numpy as np

from quantestpy import QuantestPyCircuit, assert_circuit_equivalent_to_operator
from quantestpy.exceptions import QuantestPyAssertionError


class TestAssertCircuitEquivalentToOperator(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_circuit_equivalent_to_operator.test_assert_circuit_equivalent_to_operator
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.003s

    OK
    $
    """

    def setUp(self) -> None:
        """Prepare the Bell state"""
        self.qc = QuantestPyCircuit(2)
        self.qc.add_gate(
            {"name": "h", "target_qubit": [0], "control_qubit": [],
             "control_value": [], "parameter": []})
        self.qc.add_gate(
            {"name": "x", "control_qubit": [0],  "target_qubit": [1],
             "control_value": [1], "parameter": []})

    def tearDown(self) -> None:
        del self.qc

    def test_assert_equal_to_operator_1(self,):

        expected_operator = np.array(
            [[1, 0, 1, 0],
             [0, 1, 0, 1],
             [0, 1, 0, -1],
             [1, 0, -1, 0]]
        )/np.sqrt(2.)

        self.assertIsNone(
            assert_circuit_equivalent_to_operator(
                operator_=expected_operator,
                circuit=self.qc
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
            assert_circuit_equivalent_to_operator(
                operator_=expected_operator,
                circuit=self.qc,
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
            assert_circuit_equivalent_to_operator(
                operator_=expected_operator,
                circuit=self.qc,
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
            assert_circuit_equivalent_to_operator(
                operator_=expected_operator,
                circuit=self.qc
            )
