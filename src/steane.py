import numpy as np
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


def syndrome(error: Pauli) -> tuple[int, ...]:
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
    label = stabilizer.to_label()

    if any(pauli not in "IXZ" for pauli in label):
        raise ValueError("Stabilizer must contain only I, X, and Z factors.")

    qc.h(ancilla[index])

    # qiskit Pauli labels place qubit 0 at the rightmost character.
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


def pauli_label_to_binary(label: str) -> np.ndarray:
    """
    Converts an unsigned Pauli label into binary coordinates (x | z).

    Coordinates follow the label from left to right, corresponding to
    qubits n-1, ..., 0. The label must contain only I, X, Y, and Z.
    """
    # check if the string is either empty or has some undesired characters
    if not label or any(char not in "IXYZ" for char in label):
        raise ValueError(
            "Expected a nonempty, unsigned Pauli label containing only I, X, Y, and Z."
        )

    x = np.array([char in "XY" for char in label], dtype=np.uint8)
    z = np.array([char in "YZ" for char in label], dtype=np.uint8)

    return np.concatenate((x, z))


def single_qubit_pauli_label(pauli: str, qubit_index: int, n: int = 7) -> str:
    """
    Returns the unsigned label for X, Y, or Z acting on one qubit.

    Uses qiskit's convention that the rightmost character acts on qubit 0.
    """
    if pauli not in ("X", "Y", "Z"):
        raise ValueError("pauli must be X, Y, or Z.")

    if n < 1:
        raise ValueError("n must be positive.")

    if not 0 <= qubit_index < n:
        raise ValueError("qubit_index must satisfy 0 <= qubit_index < n.")

    return "I" * (n - 1 - qubit_index) + pauli + "I" * qubit_index


# fixed binary check matrix for the ordered Steane stabilizer generators.
Steane_check_matrix = np.array(
    [pauli_label_to_binary(stabilizer.to_label()) for stabilizer in Stabilizers],
    dtype=np.uint8,
)


# symplectic form matrix Lambda = [[0, I], [I, 0]].
Lambda = np.block(
    [
        [np.zeros((7, 7), dtype=np.uint8), np.eye(7, dtype=np.uint8)],
        [np.eye(7, dtype=np.uint8), np.zeros((7, 7), dtype=np.uint8)],
    ]
)


def binary_syndrome(label: str) -> tuple[int, ...]:
    """
    Compute a Steane syndrome using binary symplectic matrix multiplication.

    The input is a seven-qubit unsigned Pauli label. Syndrome bits follow
    the order of Stabilizers.
    """
    if len(label) != 7:
        raise ValueError("Expected a seven-qubit unsigned Pauli label.")

    e = pauli_label_to_binary(label)
    syndrome_vector = (Steane_check_matrix @ Lambda @ e) % 2

    return tuple(int(bit) for bit in syndrome_vector)
