# AutoRotOrb (ARO)

AutoRotOrb is a small Python toolkit for analyzing ORCA Loewdin reduced
orbital populations and suggesting `%scf rotate` commands for active-space
calculations.

It is designed for CASSCF/NEVPT2 preparation workflows where orbitals with
large contributions from selected atoms and shells need to be moved into the
active orbital window.

## Features

- Reads ORCA output files.
- Parses `LOEWDIN REDUCED ORBITAL POPULATIONS PER MO` tables.
- Ranks molecular orbitals by selected atom/shell contributions.
- Infers inactive and active orbital ranges from `NEL` and active-electron
  counts.
- Suggests ORCA `%scf rotate` blocks.
- Supports multiple atom/orbital requests, such as metal `d`, lanthanide `f`,
  or mixed active spaces.
- Provides both a Python API and the `aro` command-line interface.

## Project Layout

```text
AutoRotOrb-ARO/
|-- autorotorb/
|   |-- __init__.py
|   |-- __main__.py
|   |-- analysis.py
|   |-- cli.py
|   |-- config.py
|   |-- io_utils.py
|   |-- models.py
|   |-- parser.py
|   |-- reporting.py
|   |-- rotation.py
|   `-- selection.py
|-- data/
|   `-- minimal_orca.out
|-- examples/
|   `-- basic_usage.py
|-- tests/
|-- main.py
|-- pyproject.toml
`-- requirements.txt
```

## Installation

ARO currently uses only the Python standard library.

For editable local development:

```bash
python -m pip install -e .
```

You can also run the package without installing it:

```bash
python -m autorotorb --help
```

## Command-Line Usage

```bash
python -m autorotorb --input data/minimal_orca.out --active-electrons 8 --orbital-request 0 Dy f 3 --spin "SPIN UP"
```

After editable installation, the same command is available as:

```bash
aro --input data/minimal_orca.out --active-electrons 8 --orbital-request 0 Dy f 3
```

Use `--spin none` to accumulate all spin blocks, or `--spin "SPIN DOWN"` to
analyze beta orbitals. Repeat `--orbital-request` for mixed active spaces.

## Python API

```python
from pathlib import Path

from autorotorb import AnalysisConfig, OrbitalRequest, analyze_active_space
from autorotorb.reporting import print_result

config = AnalysisConfig(
    output_file=Path("data/minimal_orca.out"),
    orbital_requests=[
        OrbitalRequest(atom_label="0", atom_symbol="Dy", orbital_type="f", number=3),
    ],
    active_electrons=8,
    wanted_spin="SPIN UP",
)

result = analyze_active_space(config)
print_result(result)
```

## Running Tests

```bash
python -m unittest discover
```

## Notes

- Atom labels are taken from the ORCA Loewdin table, not necessarily from the
  XYZ file.
- Molecular orbital indices follow the zero-based indices implied by ORCA's
  Loewdin population blocks.
- The active-space window inference assumes a closed inactive orbital space.
- Always inspect the resulting orbitals after applying rotations.

## License

This project is licensed under GPL-3.0-or-later. See [LICENSE](LICENSE).
