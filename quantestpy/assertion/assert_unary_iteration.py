import copy
import re
import sys
from typing import Union

import numpy as np

from quantestpy.assertion.assert_circuit_equivalent_to_output_qubit_state \
    import PauliCircuitDrawerColorErrorQubit
from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError
from quantestpy.simulator.pauli_circuit import (
    PauliCircuit, cvt_quantestpy_circuit_to_pauli_circuit)


def _is_a_in_b(a: list, b: list) -> bool:
    for i in a:
        if i in b:
            return True
    return False


def _assert_equal_qubit_state_replacing_gates_in_sys_reg_with_x_gates(
        pauli_circuit_org: PauliCircuit,
        index_reg: list,
        system_reg: list,
        in_bitstring: str,
        out_bitstring: str) -> Union[str, None]:
    # define the circuit object
    pc = copy.deepcopy(pauli_circuit_org)
    pc.set_qubit_value(index_reg, [int(i) for i in in_bitstring])

    # replace gates in system register to x-gates
    for gate_id, gate in enumerate(pc.gates):
        tgt_qubit_idx = gate["target_qubit"]
        if _is_a_in_b(a=tgt_qubit_idx, b=system_reg):
            pc.gates[gate_id]["name"] = "x"

    # execute all gates
    pc._execute_all_gates()

    # get output
    out_bitstring_actual = \
        "".join([str(i) for i in pc.qubit_value[system_reg]])

    # check out_bitstring
    if out_bitstring_actual != out_bitstring:
        return out_bitstring_actual
    else:
        return None


def _assert_ancilla_reset(pauli_circuit_org: PauliCircuit,
                          index_reg: list,
                          ancilla_reg: list,
                          in_bitstring: str) -> Union[list, None]:
    # define the circuit object
    pc = copy.deepcopy(pauli_circuit_org)
    pc.set_qubit_value(index_reg, [int(i) for i in in_bitstring])

    # execute all gates
    pc._execute_all_gates()

    # check ancilla reg
    if not np.all(pc.qubit_value[ancilla_reg] == 0):
        ancilla_err_reg = np.array(ancilla_reg)[
            pc.qubit_value[ancilla_reg] != 0].tolist()
        return ancilla_err_reg
    else:
        return None


def _draw_circuit(pauli_circuit_org: PauliCircuit,
                  index_reg: list,
                  output_reg: list,
                  output_reg_name: str,
                  in_bitstring: str,
                  err_msg: str,
                  val_err_reg: list,
                  replace_gate: bool = True) -> None:
    # define the circuit
    pc = copy.deepcopy(pauli_circuit_org)
    pc.set_qubit_value(index_reg, [int(i) for i in in_bitstring])

    # replace gates in system register to x-gates
    if replace_gate:
        for gate_id, gate in enumerate(pc.gates):
            tgt_qubit_idx = gate["target_qubit"]
            if _is_a_in_b(a=tgt_qubit_idx, b=output_reg):
                pc.gates[gate_id]["name"] = "x"

    # create an instance of PauliCircuitDrawerColorErrorQubit
    gc = PauliCircuitDrawerColorErrorQubit(
        circuit=pc,
        output_reg=output_reg,
        val_err_reg=val_err_reg,
        color_phase=False,
        phase_err_reg=[]
    )
    gc.set_name_to_reg({"in": index_reg})
    gc.set_name_to_output_reg({output_reg_name: output_reg})
    gc.draw_circuit()
    length = len(list(gc.line_id_to_text_whole.values()))
    fig = gc.create_single_string()

    # show figure
    err_msg_len = len(re.findall(r"\n{1}", err_msg)) + 1
    print(err_msg)
    print(fig)
    input("press enter")
    for _ in range(err_msg_len+length+1):
        sys.stdout.write("\033[1A\033[2K")
    del pc, gc
    return


def assert_unary_iteration(
        circuit,
        index_reg: list,
        system_reg: list,
        input_to_output: dict,
        ancilla_reg: list = [],
        draw_circuit: bool = False):
    """
    e.g.
    input_to_output = {
        "1000": "10000000",
        "1001": "11000000"
    }
    """
    quantestpy_circuit = cvt_input_circuit_to_quantestpy_circuit(circuit)
    pc_org = cvt_quantestpy_circuit_to_pauli_circuit(quantestpy_circuit)

    # check inputs
    pc_org._assert_is_correct_reg(index_reg)
    pc_org._assert_is_correct_reg(system_reg)
    pc_org._assert_is_correct_reg(ancilla_reg)
    if not isinstance(input_to_output, dict):
        raise QuantestPyError("input_to_output must be a dict.")
    if not isinstance(draw_circuit, bool):
        raise QuantestPyError("draw_circuit must be bool type.")

    len_index_reg = len(index_reg)
    len_system_reg = len(system_reg)
    for in_bitstring, out_bitstring in input_to_output.items():
        # check input type
        if not isinstance(in_bitstring, str):
            raise QuantestPyError("Input must be a binary bitstring.")
        if len(in_bitstring) != len_index_reg:
            raise QuantestPyError("Input bitstring has an invalid length.")

        # check output type
        if not isinstance(out_bitstring, str):
            raise QuantestPyError("Output must be a binary bitstring.")
        if len(out_bitstring) != len_system_reg:
            raise QuantestPyError("Output bitstring has an invalid length.")

        # check actual == expect
        return_from_assert_equal = \
            _assert_equal_qubit_state_replacing_gates_in_sys_reg_with_x_gates(
                pc_org,
                index_reg,
                system_reg,
                in_bitstring,
                out_bitstring
            )

        # actual != expect
        if return_from_assert_equal is not None:
            out_bitstring_actual = return_from_assert_equal
            err_msg = f"In bitstring: {in_bitstring}\n" \
                + f"Out bitstring expect: {out_bitstring}\n" \
                + f"Out bitstring actual: {out_bitstring_actual}"

            if draw_circuit:
                val_err_reg = []
                for i, (j, k) in enumerate(
                        zip(out_bitstring, out_bitstring_actual)):
                    if j != k:
                        val_err_reg.append(system_reg[i])

                _draw_circuit(pauli_circuit_org=pc_org,
                              index_reg=index_reg,
                              output_reg=system_reg,
                              output_reg_name="system",
                              in_bitstring=in_bitstring,
                              err_msg=err_msg,
                              val_err_reg=val_err_reg,
                              replace_gate=True)
            else:
                raise QuantestPyAssertionError(err_msg)

        # check ancilla == 0
        if len(ancilla_reg) > 0:
            return_from_assert_ancilla_reset = _assert_ancilla_reset(
                pc_org,
                index_reg,
                ancilla_reg,
                in_bitstring
            )

            # ancilla != 0
            if return_from_assert_ancilla_reset is not None:
                ancilla_err_reg = return_from_assert_ancilla_reset
                err_msg = f"In bitstring: {in_bitstring}\n" \
                    + f"Qubits {ancilla_err_reg} in ancilla reg are not" \
                    + " back to 0 by uncomputation."

                if draw_circuit:
                    _draw_circuit(pauli_circuit_org=pc_org,
                                  index_reg=index_reg,
                                  output_reg=ancilla_reg,
                                  output_reg_name="ancilla",
                                  in_bitstring=in_bitstring,
                                  err_msg=err_msg,
                                  val_err_reg=ancilla_err_reg,
                                  replace_gate=False)
                else:
                    raise QuantestPyAssertionError(err_msg)
