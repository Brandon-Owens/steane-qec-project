# steane-qec-project

## Stabilizer Syndrome Extraction Through the Lens of One-Bit QPE

This project uses the Steane $[[7,1,3]]$ quantum error-correcting code to study syndrome extraction from both the standard stabilizer-measurement perspective and the perspective of one-bit quantum phase estimation.

The project develops ancilla-based circuits for measuring the six Steane stabilizer generators and compares the resulting circuit-level syndromes with syndromes computed algebraically from Pauli commutation relations. The implementation verifies syndrome extraction for all $21$ nonidentity single-qubit Pauli errors.

Later stages of the project reinterpret stabilizer measurement as one-bit quantum phase estimation and introduce the binary symplectic representation of Pauli operators and stabilizers. This provides an efficient linear-algebraic description of commutation and syndrome information and establishes machinery that will be reused in Project 2.

## Project Structure

- `src/steane.py` contains the Steane stabilizer generators together with the algebraic syndrome function and ancilla-based stabilizer-measurement routines.
- `tests/test_steane.py` contains automated tests for the stabilizer generators, algebraic syndromes, stabilizer-measurement circuits, and agreement between circuit-based and algebraic syndrome extraction.
- `notebooks/steane_syndrome_extraction.ipynb` develops the mathematical background and demonstrates syndrome extraction for the Steane code step by step.
- `pyproject.toml` and `uv.lock` specify the project environment and dependencies.

## Current Status

The first stage of the project is complete. The repository currently includes the Steane stabilizer generators, algebraic syndrome computation, ancilla-based measurement of individual stabilizers, full six-bit syndrome extraction, preparation of the logical state $|0_L\rangle$, and verification that the circuit-level syndrome agrees with the algebraic syndrome for all $21$ nonidentity weight-one Pauli errors.

The next stage will reinterpret the stabilizer-measurement circuit as one-bit quantum phase estimation.

## Setup and Reproducibility

This project uses [uv](https://docs.astral.sh/uv/) for Python environment and dependency management. The required runtime and development dependencies are recorded in `pyproject.toml`, with exact resolved versions stored in `uv.lock`.

After cloning the repository, create and synchronize the project environment with

```bash
uv sync --locked
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

The main notebook is located at

```text
notebooks/steane_syndrome_extraction.ipynb
```

When opening the notebook in VS Code or Jupyter, select the Python interpreter from the project environment:

```text
.venv/bin/python
```

This ensures that the notebook uses the same locked environment as the source code and test suite.

## Testing and Verification

The automated test suite checks both the algebraic and circuit-level components of the implementation. In particular, it verifies that:

- the six chosen Steane stabilizer generators commute and form an independent generating set;
- the $21$ nonidentity weight-one Pauli errors have distinct, nonzero syndromes;
- the ancilla-based circuits correctly distinguish the $+1$ and $-1$ eigenspaces of both $X$-type and $Z$-type stabilizer generators; and
- the full six-bit syndrome obtained from circuit simulation agrees with the algebraic syndrome for every weight-one Pauli error.

Together, these tests provide an automated consistency check between the stabilizer algebra and the corresponding Qiskit circuits.

## Conventions

Qiskit represents Pauli strings with qubit $0$ at the rightmost position. For example,

$$
\mathtt{IIIXXXX}
$$

acts nontrivially on data qubits $0,1,2,3$.

Syndromes are written in stabilizer-generator order,

$$
(s_1,\ldots,s_6),
$$

while Qiskit displays classical measurement bitstrings with the highest-index classical bit on the left. Circuit-generated bitstrings are therefore reversed before comparison with the algebraic syndrome representation.
