# steane-qec-project

## Stabilizer Syndrome Extraction, One-Bit QPE, and the Binary Symplectic Formalism

This project studies syndrome extraction for the Steane $[[7,1,3]]$ quantum error-correcting code through three complementary approaches: ancilla-based stabilizer measurements, one-bit quantum phase estimation (QPE), and binary symplectic linear algebra.

The implementation verifies that circuit-based syndrome extraction agrees with algebraic syndrome calculations for all 21 single-qubit Pauli errors. The accompanying notebooks develop the connection between stabilizer measurement and one-bit QPE, then express the same Pauli commutation and syndrome structure through binary matrix operations over $\mathbb{F}\_2$.

## Project Structure

The project consists of three notebooks, intended to be read in order:

1. [**Steane Syndrome Extraction**](notebooks/steane_syndrome_extraction.ipynb) — Introduces the stabilizer formalism and demonstrates ancilla-based syndrome extraction.
2. [**Stabilizer Measurement as One-Bit QPE**](notebooks/stabilizer_measurement_as_qpe.ipynb) — Derives the QPE interpretation of stabilizer measurement and verifies the resulting syndromes.
3. [**Binary Symplectic Representation**](notebooks/binary_symplectic_representation.ipynb) — Develops the binary representation of Pauli operators, constructs the Steane CSS check matrices, and verifies binary syndrome calculations.

Supporting files:

- [`src/steane.py`](src/steane.py) — Stabilizer generators, algebraic syndrome computation, and measurement circuits.
- [`tests/test_steane.py`](tests/test_steane.py) — Automated algebraic and circuit-level tests.
- `pyproject.toml` and `uv.lock` — Project dependencies and reproducible environment.

## Setup and Reproducibility

This project uses [uv](https://docs.astral.sh/uv/) for dependency management, with Python 3.12 selected in `.python-version` and dependencies recorded in `pyproject.toml` and `uv.lock`.

To install the dependencies and launch JupyterLab, run from the repository root:

```bash
uv sync --locked
uv run jupyter lab
```

The notebooks are located in `notebooks/`. If prompted, select `.venv/bin/python` as the notebook kernel.

To run the automated tests and Ruff checks:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Testing and Verification

The automated test suite checks both the algebraic and circuit-level components of the implementation. In particular, it verifies that:

- the six chosen Steane stabilizer generators commute and form an independent generating set;
- the $21$ weight-one Pauli errors have distinct, nonzero syndromes;
- the ancilla-based circuits correctly distinguish the $+1$ and $-1$ eigenspaces of both $X$-type and $Z$-type stabilizer generators; and
- the full six-bit syndrome obtained from circuit simulation agrees with the algebraic syndrome for every weight-one Pauli error.

The QPE and binary symplectic notebooks provide additional computational checks. The QPE notebook independently constructs one-bit QPE-based syndrome-extraction circuits, while the binary symplectic notebook computes syndromes through binary matrix operations over $\mathbb{F}_2$. Both approaches reproduce the algebraic syndromes for all $21$ weight-one Pauli errors.

## Conventions

We follow Qiskit's qubit-ordering convention: an $n$-qubit Pauli label is written as $P_{n-1}\cdots P_1P_0$, with qubit $0$ at the rightmost position. For example, `IIIXXXX` acts nontrivially on qubits $0,1,2,3$.

Syndromes are written in stabilizer-generator order, $(s_1,\ldots,s_6)$, with $s_i=0$ for commuting and $s_i=1$ for anticommuting errors. Since Qiskit displays classical measurement bitstrings with the highest-index bit on the left, these bitstrings are reversed before comparison with algebraic syndromes.

## Scope and Limitations

The implementation is specific to the Steane $[[7,1,3]]$ code and accepts seven-qubit Qiskit Pauli objects for algebraic syndrome calculations. Full circuit-based syndrome extraction uses seven data qubits, six ancilla qubits, and six classical syndrome bits.

Circuit simulations assume ideal, noiseless operations. The project implements syndrome extraction but not error recovery or decoding. Logical state preparation uses Qiskit's built-in `synth_circuit_from_stabilizers` routine rather than a custom encoding circuit.
