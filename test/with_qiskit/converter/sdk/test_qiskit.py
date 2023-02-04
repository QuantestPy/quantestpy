import traceback
import unittest

import numpy as np
from qiskit import QuantumCircuit

from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.converter.sdk.qiskit import _IMPLEMENTED_QISKIT_GATES
from quantestpy.exceptions import QuantestPyError
from quantestpy.simulator.state_vector_circuit import \
    cvt_quantestpy_circuit_to_state_vector_circuit


class TestQiskit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.with_qiskit.converter.sdk.test_qiskit
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    OK
    """

    def test_error_msg(self,):
        qc = QuantumCircuit(3)
        qc.rxx(np.pi/4, 0, 1)

        try:
            qpc = cvt_input_circuit_to_quantestpy_circuit(qc)
            svc = cvt_quantestpy_circuit_to_state_vector_circuit(qpc)
            return svc

        except QuantestPyError as e:

            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyError: " \
                + "Qiskit gate [rxx] is not supported in QuantestPy.\n" \
                + f'Implemented qiskit gates: {_IMPLEMENTED_QISKIT_GATES}\n'

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]
            print(actual_error_msg)
            self.assertEqual(expected_error_msg, actual_error_msg)
