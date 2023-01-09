import traceback
import unittest

from quantestpy import StateVectorCircuit
from quantestpy.simulator.exceptions import StateVectorCircuitError


class TestStateVectorCircuitAddGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.state_vector_circuit.test_add_gate
    ................
    ----------------------------------------------------------------------
    Ran 16 tests in 0.001s

    OK
    $
    """

    def test_parameter_without_param(self,):
        svc = StateVectorCircuit(1)

        try:
            self.assertIsNotNone(
                svc.add_gate(
                    {"name": "x",
                     "target_qubit": [0],
                     "control_qubit": [],
                     "control_value": [],
                     "parameter": [1]}
                )
            )

        except StateVectorCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.StateVectorCircuitError: " \
                + "x gate must have " \
                + "an empty list for 'parameter'.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_parameter_with_one_param(self,):
        svc = StateVectorCircuit(1)

        try:
            self.assertIsNotNone(
                svc.add_gate(
                    {"name": "p",
                     "target_qubit": [0],
                     "control_qubit": [],
                     "control_value": [],
                     "parameter": []}
                )
            )

        except StateVectorCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.StateVectorCircuitError: " \
                + "p gate must have a list containing " \
                + "exactly 1 element for 'parameter'.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_parameter_with_four_param(self,):
        svc = StateVectorCircuit(1)

        try:
            self.assertIsNotNone(
                svc.add_gate(
                    {"name": "u",
                     "target_qubit": [0],
                     "control_qubit": [],
                     "control_value": [],
                     "parameter": []}
                )
            )

        except StateVectorCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.StateVectorCircuitError: " \
                + "u gate must have a list containing " \
                + "exactly 4 elements for 'parameter'.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_value_type_in_parameter(self,):
        svc = StateVectorCircuit(1)

        try:
            self.assertIsNotNone(
                svc.add_gate(
                    {"name": "p",
                     "target_qubit": [0],
                     "control_qubit": [],
                     "control_value": [],
                     "parameter": ["a"]}
                )
            )

        except StateVectorCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.StateVectorCircuitError: " \
                + "Parameter(s) in p gate must be float or integer type.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)
