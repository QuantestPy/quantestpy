import traceback
import unittest

from quantestpy.converter.sdk.qasm import _cvt_openqasm_to_quantestpy_circuit
from quantestpy.exceptions import QuantestPyError


class TestConverterWithoutQiskit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m \
        unittest test.converter.qasm.test_converter_without_qiskit
    ...
    ----------------------------------------------------------------------
    Ran 5 tests in 0.041s

    OK
    """

    def test_error_msg_without_qiskit(self,):
        qasm = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[2];\nx q[0];\n'

        with self.assertRaises(QuantestPyError):
            _ = _cvt_openqasm_to_quantestpy_circuit(qasm)

        try:
            _ = _cvt_openqasm_to_quantestpy_circuit(qasm)

        except QuantestPyError as e:
            expected_error_msg = "quantestpy.exceptions.QuantestPyError: " \
                + "Qiskit is missing. Please install it.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)
