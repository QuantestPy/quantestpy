import copy
import re
import sys

import numpy as np

from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError
from quantestpy.simulator.pauli_circuit import (
    PauliCircuit, cvt_quantestpy_circuit_to_pauli_circuit)
from quantestpy.visualization.pauli_circuit_drawer import PauliCircuitDrawer


class PauliCircuitDrawerColorErrorQubit(PauliCircuitDrawer):
    def __init__(self,
                 circuit: PauliCircuit,
                 output_reg: list,
                 val_err_reg: list,
                 color_phase: bool,
                 phase_err_reg: list):
        super().__init__(circuit)
        # new attributes
        self._output_reg = output_reg
        self._val_err_reg = val_err_reg
        self._color_phase = color_phase
        self._phase_err_reg = phase_err_reg
        self._color_code_succ = self.get_color_code("cyan")
        self._color_code_err = self.get_color_code("red")

    def draw_final_vector(self) -> None:
        """Overrides :
        Colors as well as draws final state vectors.
        """
        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                qubit_id = self._line_id_to_qubit_id[line_id]
                qubit_val = self._qc.qubit_value[qubit_id]
                if qubit_id in self._val_err_reg:
                    cc = self._color_code_err
                elif qubit_id in self._output_reg:
                    cc = self._color_code_succ
                else:
                    cc = ""
                obj = self.get_state(qubit_val)
                obj = self.add_color_code_in_obj(cc, obj)
            else:
                obj = self.get_space(length=3)
            self.add_obj_in_line_id_to_text(line_id, obj)

    def draw_final_phase(self) -> None:
        """Overrides :
        Colors as well as draws qubit phases in unit of PI.
        """
        phase_max_length = 0
        for qubit_phase in self._qc.qubit_phase:
            phase_length = len(self.get_phase(qubit_phase))
            if phase_length > phase_max_length:
                phase_max_length = phase_length

        for line_id in range(self._num_line):
            if line_id in self._line_id_to_qubit_id.keys():
                qubit_id = self._line_id_to_qubit_id[line_id]
                qubit_phase = self._qc.qubit_phase[qubit_id]
                if qubit_id in self._phase_err_reg and self._color_phase:
                    cc = self._color_code_err
                elif qubit_id in self._output_reg and self._color_phase:
                    cc = self._color_code_succ
                else:
                    cc = ""
                phase = self.get_phase(qubit_phase)
                obj = phase + self.get_space(phase_max_length-len(phase))
                obj = self.add_color_code_in_obj(cc, obj)
            else:
                obj = self.get_space(length=phase_max_length)
            self.add_obj_in_line_id_to_text(line_id, obj)


def _assert_internal(pauli_circuit_org: PauliCircuit,
                     input_reg: list,
                     output_reg: list,
                     in_bitstring: str,
                     out_bitstring: str,
                     out_phase: list):
    # define the circuit object
    pc = copy.deepcopy(pauli_circuit_org)
    pc.set_qubit_value(input_reg, [int(i) for i in in_bitstring])
    pc._execute_all_gates()

    # get output
    out_bitstring_actual = \
        "".join([str(i) for i in pc.qubit_value[output_reg]])
    out_phase_actual = (pc.qubit_phase[output_reg] / np.pi).tolist()
    del pc

    if out_bitstring_actual != out_bitstring:
        return out_bitstring_actual, out_phase_actual
    elif len(out_phase) > 0 and out_phase_actual != out_phase:
        return out_bitstring_actual, out_phase_actual
    else:
        return None


def _draw_circuit(pauli_circuit_org: PauliCircuit,
                  input_reg: list,
                  output_reg: list,
                  in_bitstring: str,
                  err_msg: str,
                  val_err_reg: list,
                  color_phase: bool,
                  phase_err_reg: list) -> None:
    # define the circuit
    pc = copy.deepcopy(pauli_circuit_org)
    pc.set_qubit_value(input_reg, [int(i) for i in in_bitstring])

    # create an instance of CircuitDrawer
    gc = PauliCircuitDrawerColorErrorQubit(
        pc, output_reg, val_err_reg, color_phase, phase_err_reg)
    gc.set_name_to_reg({"in": input_reg})
    gc.set_name_to_output_reg({"out": output_reg})
    gc.draw_circuit()
    length = len(list(gc.line_id_to_text_whole.values()))
    fig = gc.create_single_string()

    # show result
    err_msg_len = len(re.findall(r"\n{1}", err_msg)) + 1
    print(err_msg)
    print(fig)
    input("press enter")
    for _ in range(err_msg_len+length+1):
        sys.stdout.write("\033[1A\033[2K")
    del pc, gc
    return


def assert_circuit_equivalent_to_output_qubit_state(
        circuit,
        input_reg: list,
        output_reg: list,
        input_to_output: dict,
        draw_circuit: bool = False):
    """
    e.g.
    input_to_output = {
        "1000": ("100000", [0.5,0,0,0,0,0]),
        "1001": "100001"
    }
    """
    quantestpy_circuit = cvt_input_circuit_to_quantestpy_circuit(circuit)
    pc_org = cvt_quantestpy_circuit_to_pauli_circuit(quantestpy_circuit)

    # check inputs
    pc_org._assert_is_correct_reg(input_reg)
    pc_org._assert_is_correct_reg(output_reg)
    if not isinstance(input_to_output, dict):
        raise QuantestPyError("input_to_output must be a dict.")
    if not isinstance(draw_circuit, bool):
        raise QuantestPyError("draw_circuit must be bool type.")

    len_input_reg = len(input_reg)
    len_output_reg = len(output_reg)

    for in_bitstring, output in input_to_output.items():
        # check input type
        if not isinstance(in_bitstring, str):
            raise QuantestPyError("Input must be a binary bitstring.")
        if len(in_bitstring) != len_input_reg:
            raise QuantestPyError("Input bitstring has an invalid length.")

        # check output type
        if not isinstance(output, str) and not isinstance(output, tuple):
            raise QuantestPyError(
                "Output must be either a binary bitstring or a tuple "
                "having both a binary bitstring and a list of qubit phases."
            )
        if isinstance(output, str):
            out_bitstring = output
            out_phase = []
        else:
            out_bitstring, out_phase = output
            if not isinstance(out_phase, list):
                raise QuantestPyError(
                    "qubit phases must be given by a list in a tuple."
                )
            if len(out_phase) != len_output_reg:
                raise QuantestPyError(
                    "List of qubit phases has an invalid length."
                )
        if len(out_bitstring) != len_output_reg:
            raise QuantestPyError("Output bitstring has an invalid length.")

        # check equalness
        return_from_assert_internal = _assert_internal(pc_org,
                                                       input_reg,
                                                       output_reg,
                                                       in_bitstring,
                                                       out_bitstring,
                                                       out_phase)

        if return_from_assert_internal is not None:
            out_bitstring_actual, out_phase_actual \
                = return_from_assert_internal

            err_msg = f"In bitstring: {in_bitstring}\n" \
                + f"Out bitstring expect: {out_bitstring}\n" \
                + f"Out bitstring actual: {out_bitstring_actual}"

            if len(out_phase) > 0:
                err_msg += f"\nOut phase expect: {out_phase}\n" \
                    + f"Out phase actual: {out_phase_actual}"

            if draw_circuit:
                # collect err qubit ids
                val_err_reg, phase_err_reg = [], []
                for i, (j, k) in enumerate(
                        zip(out_bitstring, out_bitstring_actual)):
                    if j != k:
                        val_err_reg.append(output_reg[i])

                if len(out_phase) > 0:
                    color_phase = True
                    for i, (j, k) in enumerate(
                            zip(out_phase, out_phase_actual)):
                        if j != k:
                            phase_err_reg.append(output_reg[i])
                else:
                    color_phase = False

                _draw_circuit(pc_org,
                              input_reg,
                              output_reg,
                              in_bitstring,
                              err_msg,
                              val_err_reg,
                              color_phase,
                              phase_err_reg)

            else:
                raise QuantestPyAssertionError(err_msg)
