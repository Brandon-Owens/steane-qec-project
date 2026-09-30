from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.circuit import AncillaRegister
from qiskit.quantum_info import Pauli

# define our stabilizer generators for the Steane [[7,1,3]] code
Stabilizers = [
    Pauli("IIIXXXX"),
    Pauli("IXXIIXX"),
    Pauli("XIXIXIX"),
    Pauli("IIIZZZZ"),
    Pauli("IZZIIZZ"),
    Pauli("ZIZIZIZ"),
]


def syndrome(error: Pauli) -> tuple[int, int, int, int, int, int]:
    """
    Compute the syndrome of a Pauli error with respect to the six
    Steane stabilizer generators.

    A syndrome bit is 0 if the error commutes with the corresponding
    stabilizer generator and 1 if it anticommutes.
    """
    return tuple(0 if error.commutes(stabilizer) else 1 for stabilizer in Stabilizers)


def measure_stabilizer(
    qc: QuantumCircuit,
    data: QuantumRegister,
    ancilla: AncillaRegister,
    syndrome_bits: ClassicalRegister,
    stabilizer: Pauli,
    index: int,
) -> None:
    """
    Append an ancilla-based measurement of one Steane stabilizer.

    The circuit is modified in place. The ancilla and classical bit at
    `index` store the measurement associated with the supplied stabilizer.

    Assumes the stabilizer contains only I, X, and Z factors and uses
    Qiskit's convention that qubit 0 is the rightmost Pauli-string entry.
    """
    qc.h(ancilla[index])

    label = stabilizer.to_label()

    # Qiskit Pauli labels place qubit 0 at the rightmost character.
    for qubit_index, pauli in enumerate(reversed(label)):
        if pauli == "X":
            qc.cx(ancilla[index], data[qubit_index])
        elif pauli == "Z":
            qc.cz(ancilla[index], data[qubit_index])

    qc.h(ancilla[index])
    qc.measure(ancilla[index], syndrome_bits[index])


def append_syndrome_measurement(
    qc: QuantumCircuit,
    data: QuantumRegister,
    ancilla: AncillaRegister,
    syndrome_bits: ClassicalRegister,
) -> None:
    """
    Append measurements of all six Steane stabilizer generators.

    The circuit is modified in place. The implementation requires a
    seven-qubit data register, six ancilla qubits, and six classical
    syndrome bits.
    """
    for index, stabilizer in enumerate(Stabilizers):
        measure_stabilizer(
            qc,
            data,
            ancilla,
            syndrome_bits,
            stabilizer,
            index,
        )
