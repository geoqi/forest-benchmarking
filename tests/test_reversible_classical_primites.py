"""
Test over all inputs
"""
from pyquil.api import QVMConnection
from pyquil.quil import Program
from pyquil.gates import X, I, CNOT, CCNOT
from forest_benchmarking.benchmarks.classical_logic_circuits\
    .classical_reversible_logic_primitives import (unmajority_add_gate,
                                                   unmajority_add_parallel_gate, majority_gate)

qvm = QVMConnection()

def test_majority_gate():
    """
    Testing the majority gate with a truth table
    """
    true_truth_table = {(0, 0, 0): (0, 0, 0),
                        (0, 0, 1): (1, 1, 0),
                        (0, 1, 0): (0, 1, 0),
                        (0, 1, 1): (1, 0, 1),
                        (1, 0, 0): (1, 0, 0),
                        (1, 0, 1): (0, 1, 1),
                        (1, 1, 0): (1, 1, 1),
                        (1, 1, 1): (0, 0, 1)}

    maj_gate_program = majority_gate(0, 1, 2)
    for key, value in true_truth_table.items():
        state_prep_prog = Program().inst(I(2))
        for qbit_idx, bit in enumerate(key):
            if bit == 1:
                state_prep_prog += X(qbit_idx)

        result = qvm.run_and_measure(state_prep_prog + maj_gate_program,
                                     list(range(3)), trials=1)
        assert tuple(result[0]) == true_truth_table[key]

def test_unmajority_add_gate():
    """
    Testing the Unmajority add gate with a truth table
    """
    true_truth_table = {(0, 0, 0): (0, 0, 0),
                        (0, 0, 1): (1, 1, 1),
                        (0, 1, 0): (0, 1, 0),
                        (0, 1, 1): (1, 0, 1),
                        (1, 0, 0): (1, 1, 0),
                        (1, 0, 1): (0, 0, 1),
                        (1, 1, 0): (0, 1, 1),
                        (1, 1, 1): (1, 0, 0)}

    unmaj_add_gate_program = unmajority_add_gate(0, 1, 2)
    for key, value in true_truth_table.items():
        state_prep_prog = Program().inst(I(2))
        for qbit_idx, bit in enumerate(key):
            if bit == 1:
                state_prep_prog += X(qbit_idx)

        result = qvm.run_and_measure(state_prep_prog + unmaj_add_gate_program,
                                     list(range(3)), trials=1)
        assert tuple(result[0]) == true_truth_table[key]

def test_composition_of_majority_and_unmajority_gates():
    """
    Testing the composition of the majority gate with the unmajority add gate with a truth table
    """
    true_truth_table = {(0, 0, 0): (0, 0, 0),
                        (0, 0, 1): (0, 1, 1),
                        (0, 1, 0): (0, 1, 0),
                        (0, 1, 1): (0, 0, 1),
                        (1, 0, 0): (1, 1, 0),
                        (1, 0, 1): (1, 0, 1),
                        (1, 1, 0): (1, 0, 0),
                        (1, 1, 1): (1, 1, 1)}

    compose_maj_and_unmaj_gate_program = majority_gate(0, 1, 2) + unmajority_add_gate(0, 1, 2)
    for key, value in true_truth_table.items():
        state_prep_prog = Program().inst(I(2))
        for qbit_idx, bit in enumerate(key):
            if bit == 1:
                state_prep_prog += X(qbit_idx)

        result = qvm.run_and_measure(state_prep_prog + compose_maj_and_unmaj_gate_program,
                                     list(range(3)), trials=1)
        assert tuple(result[0]) == true_truth_table[key]