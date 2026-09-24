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


def syndrome(error):
    # loops through each stabilizer generator in Stabilizers and computes the syndrome for that particular generator-error pair, returning a tuple
    return tuple(0 if error.commutes(stabilizer) else 1 for stabilizer in Stabilizers)
