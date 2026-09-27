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
    qc,
    data,
    ancilla,
    syndrome_bits,
    stabilizer,
    index,
):
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


def append_syndrome_measurement(qc, data, ancilla, syndrome_bits):
    for index, stabilizer in enumerate(Stabilizers):
        measure_stabilizer(
            qc,
            data,
            ancilla,
            syndrome_bits,
            stabilizer,
            index,
        )
