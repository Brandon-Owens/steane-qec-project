# steane-qec-project

## Stabilizer Syndrome Extraction, One-Bit QPE, and the Binary Symplectic Formalism

This project uses the Steane $[[7,1,3]]$ quantum error-correcting code to study stabilizer syndrome extraction from several complementary perspectives.

The project develops the stabilizer and syndrome formalism, implements ancilla-based circuits for measuring the six Steane stabilizer generators, and verifies syndrome extraction for all $21$ weight-one Pauli errors. It then interprets stabilizer measurement as one-bit quantum phase estimation, connecting the standard syndrome-extraction circuit to the phase-estimation framework developed earlier in the project.

Finally, the project translates the Pauli and stabilizer formalism into binary linear algebra over $\mathbb{F}_2$ using the binary symplectic representation. In this framework, stabilizer commutation and syndrome computation are expressed in terms of binary check matrices and symplectic products, providing an independent algebraic description of the same Steane syndrome structure.

## Project Structure

- `src/steane.py` contains the Steane stabilizer generators together with the algebraic syndrome function and ancilla-based stabilizer-measurement routines.
- `tests/test_steane.py` contains automated tests for the stabilizer generators, algebraic syndromes, stabilizer-measurement circuits, and agreement between circuit-based and algebraic syndrome extraction.
- `notebooks/steane_syndrome_extraction.ipynb` develops the stabilizer and syndrome formalism and demonstrates conventional ancilla-based syndrome extraction.
- `notebooks/stabilizer_measurement_as_qpe.ipynb` develops the interpretation of stabilizer measurement as one-bit quantum phase estimation and compares QPE-based syndrome extraction with the algebraic syndrome calculation.
- `notebooks/binary_symplectic_representation.ipynb` develops the binary symplectic representation of Pauli operators modulo phase, constructs the Steane stabilizer check matrix and its CSS block structure, expresses stabilizer commutation and syndrome computation as binary matrix operations, and verifies the resulting syndromes for all $21$ weight-one Pauli errors.
- `pyproject.toml` and `uv.lock` specify the project environment and dependencies.

The notebooks are intended to be read in the order listed above. The first develops the stabilizer and syndrome-extraction framework used throughout the project, the second reinterprets stabilizer measurement through one-bit QPE, and the third translates the same Pauli-commutation and syndrome structure into the binary symplectic formalism.

## Setup and Reproducibility

This project uses [uv](https://docs.astral.sh/uv/) for Python environment and dependency management. The required runtime and development dependencies are recorded in `pyproject.toml`, with exact resolved versions stored in `uv.lock`.

After cloning the repository, create and synchronize the project environment with

```bash
uv sync --locked
```

To launch JupyterLab using the project environment,

```bash
uv run jupyter lab
```

The `dev` dependency group is included by default by `uv`, so this installs the packages required for testing, linting, notebook execution, and circuit visualization in addition to the core project dependencies.

To run the automated test suite,

```bash
uv run pytest
```

To run the Ruff checks,

```bash
uv run ruff check .
uv run ruff format --check .
```

The project notebooks are located at

- `notebooks/steane_syndrome_extraction.ipynb`
- `notebooks/stabilizer_measurement_as_qpe.ipynb`
- `notebooks/binary_symplectic_representation.ipynb`

When opening a notebook in VS Code or Jupyter, select the Python interpreter from the project environment:

```text
.venv/bin/python
```

This ensures that the notebook uses the same locked environment as the source code and test suite.

## Testing and Verification

The automated test suite checks both the algebraic and circuit-level components of the implementation. In particular, it verifies that:

- the six chosen Steane stabilizer generators commute and form an independent generating set;
- the $21$ weight-one Pauli errors have distinct, nonzero syndromes;
- the ancilla-based circuits correctly distinguish the $+1$ and $-1$ eigenspaces of both $X$-type and $Z$-type stabilizer generators; and
- the full six-bit syndrome obtained from circuit simulation agrees with the algebraic syndrome for every weight-one Pauli error.

Together, these tests provide an automated consistency check between the stabilizer algebra and the corresponding Qiskit circuits.

The QPE notebook provides an additional independent computational validation: its QPE-based syndrome extraction agrees with the algebraic syndrome for all $21$ weight-one Pauli errors.

The binary symplectic notebook provides a further algebraic cross-check. Writing

$$
v([E])=(\mathbf{x}\mid\mathbf{z})\in\mathbb{F}_2^{2n}
$$

for the binary symplectic representation of a Pauli error modulo phase, and defining

$$
\Lambda=
\begin{pmatrix}
0 & I_n \\
I_n & 0 \\
\end{pmatrix},
$$

the syndrome is computed as

$$
s(E)=H\Lambda v([E])^T.
$$

For all $21$ weight-one Pauli errors, this binary symplectic syndrome calculation agrees with the syndrome obtained directly from Pauli commutation relations.

## Conventions

Qiskit represents an $n$-qubit Pauli string with qubit $0$ at the rightmost position. Accordingly, throughout this project an $n$-qubit Pauli operator is written as

$$
P=i^\ell P\_{n-1}\otimes\cdots\otimes P_1\otimes P_0,
$$

where each $P_j\in{I,X,Y,Z}$ acts on qubit $j$.

For example,

$$
\mathtt{IIIXXXX}
$$

represents

$$
I_6\otimes I_5\otimes I_4\otimes X_3\otimes X_2\otimes X_1\otimes X_0,
$$

and therefore acts nontrivially on data qubits $0,1,2,3$.

This left-to-right Qiskit ordering is used consistently throughout all project notebooks. In particular, the binary symplectic coordinates follow the same displayed qubit order as the Qiskit Pauli strings. Modulo phase, a Pauli operator is represented by

$$
(x\_{n-1},\ldots,x_1,x_0
\mid
z\_{n-1},\ldots,z_1,z_0)
\in\mathbb{F}\_2^{2n},
$$

where the pair $(x_j,z_j)$ specifies the Pauli acting on qubit $j$ according to

$$
I\leftrightarrow(0,0),\qquad
X\leftrightarrow(1,0),\qquad
Z\leftrightarrow(0,1),\qquad
Y\leftrightarrow(1,1).
$$

Thus the displayed binary coordinates are ordered as

$$
q\_{n-1},\ldots,q_1,q_0,
$$

so that their order agrees directly with the characters of a Qiskit Pauli label.

For the Steane code, for example,

$$
S_1=\mathtt{IIIXXXX}
$$

has binary symplectic representation

$$
(0,0,0,1,1,1,1
\mid
0,0,0,0,0,0,0).
$$

Syndromes are written in stabilizer-generator order,

$$
(s_1,\ldots,s_6),
$$

while Qiskit displays classical measurement bitstrings with the highest-index classical bit on the left. Circuit-generated bitstrings are therefore reversed before comparison with the algebraic syndrome representation.

## Supported Inputs

The current implementation is specialized to the Steane $[[7,1,3]]$ code and the six stabilizer generators defined in `src/steane.py`. Algebraic syndrome calculations accept seven-qubit Qiskit `Pauli` objects.

The single-stabilizer measurement routine requires a seven-qubit data register, an ancilla register, and a classical syndrome register. Full syndrome extraction uses seven data qubits, six ancilla qubits, and six classical syndrome bits.

## Known Limitations

- The current implementation is specific to the Steane $[[7,1,3]]$ code rather than a general stabilizer-code framework.
- Circuit simulations use an ideal noiseless simulator and do not model hardware noise or connectivity constraints.
- The project currently performs syndrome extraction but does not implement error recovery or correction.
- The logical state $|0_L\rangle$ is prepared using Qiskit's built-in `synth_circuit_from_stabilizers` routine rather than a custom encoding circuit.
