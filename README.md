# 🌀 AutoRotOrb (ARO): Automatic Orbital Rotation Helper for ORCA Active Spaces

AutoRotOrb (ARO) is a lightweight Python toolkit for analyzing ORCA Löwdin reduced orbital populations and suggesting orbital rotations for active-space calculations.

It is especially useful when preparing or refining CASSCF/NEVPT2 active spaces, where orbitals with strong contributions from selected atoms and shells must be brought into the active orbital window.

---

## ⚙️ Features

* 📄 **Reads ORCA output files**
* 🔎 **Parses Löwdin reduced orbital populations per molecular orbital**
* 🧠 **Ranks molecular orbitals by selected atom/orbital contributions**
* 🧮 **Infers inactive and active orbital ranges from NEL and active electron count**
* 🔁 **Suggests ORCA `%scf rotate` commands**
* 🧩 Supports multiple atom/orbital requests, such as metal `d` orbitals, lanthanide `f` orbitals, or mixed active spaces
* 🖥️ Can be executed through `main.py`, `python -m autorotorb`, or the `aro` command after installation

---

## 📁 Structure

```text
AutoRotOrb-ARO/
├── main.py                    # Main runner script
├── config/
│   ├── __init__.py
│   └── config.py              # User settings for main.py
├── pyproject.toml             # Package metadata and CLI entry point
├── src/
│   └── autorotorb/
│       ├── __init__.py         # Package exports
│       ├── __main__.py         # Enables python -m autorotorb
│       ├── cli.py              # Command-line interface
│       ├── config.py           # User-facing configuration dataclasses
│       ├── models.py           # Internal result/data structures
│       ├── io_utils.py         # File-reading utilities
│       ├── parser.py           # ORCA Löwdin population parser
│       ├── selection.py        # Orbital ranking and candidate selection
│       ├── rotation.py         # Orbital swap detection and rotate block creation
│       ├── analysis.py         # Full active-space analysis pipeline
│       └── reporting.py        # Text report generation
├── examples/
│   └── basic_usage.py          # Minimal usage example
├── tests/                      # Unit tests and fixtures
└── data/                       # Place ORCA output files here
```

---

## ▶️ How to Use

### 1. Install Requirements

ARO currently uses only the Python standard library.

```bash
python --version
```

Python 3.9 or newer is recommended.

For editable local installation:

```bash
python -m pip install -e .
```

### 2. Add Your ORCA Output File

Place your ORCA output file inside the `data/` folder. Example:

```text
data/example.out
```

The file must contain the ORCA section:

```text
LOEWDIN REDUCED ORBITAL POPULATIONS PER MO
```

### 3. Configure `config/config.py`

```python
ANALYSIS_CONFIG = AnalysisConfig(
    output_file=Path("data/example.out"),
    orbital_requests=[
        OrbitalRequest(atom_label="0", atom_symbol="Dy", orbital_type="f", number=7),
    ],
    active_electrons=9,
    wanted_spin="SPIN UP",
)
```

Each `OrbitalRequest` defines an atom/shell contribution to track.

### 4. Run

```bash
python main.py
```

ARO prints the inferred active-space window, selected candidate molecular orbitals, current active-space orbital indices, and suggested ORCA `%scf rotate` commands.

You can also run the command-line interface:

```bash
python -m pip install -e .
python -m autorotorb --input data/example.out --active-electrons 9 --orbital-request 0 Dy f 7 --spin "SPIN UP"
```

After editable installation, the same command is available as:

```bash
aro --input data/example.out --active-electrons 9 --orbital-request 0 Dy f 7 --spin "SPIN UP"
```

---

## 🧪 Tests

Run the unit tests with:

```bash
python -m pip install -e .
python -m unittest discover
```

---

## 📌 Notes

* Atom labels are taken from the ORCA Löwdin table, not necessarily from the XYZ file.
* Molecular orbital indices follow the indices printed in the ORCA population blocks.
* `wanted_spin` can be `"SPIN UP"`, `"SPIN DOWN"`, or `None`.
* The method assumes a closed inactive orbital space when inferring the active orbital window.
* Always inspect the resulting orbitals after applying rotations.

---

## 👨‍🔬 Applications

ARO was designed for workflows involving:

* CASSCF active-space preparation
* NEVPT2 calculations
* transition-metal complexes
* lanthanide complexes
* orbital localization and active-space troubleshooting

---

## 👤 Author

Lucas Gian Fachini – *PhD Candidate in Inorganic and Theoretical Chemistry*  
[GitHub: lgfachini](https://github.com/lgfachini)

---

## 📄 License

This project is licensed under the GPL-3.0 License.

---

## 💡 Acknowledgments

This project uses concepts from ORCA molecular orbital population analysis, active-space selection in multireference quantum chemistry, and orbital rotation procedures for CASSCF calculations.
