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
* 🖥️ **Command-line interface** (`aro` or `python -m autorotorb.cli`)
* 🧪 **Unit tests** with a minimal ORCA fixture for CI and local checks

---

## 📁 Structure

```text
AutoRotOrb-ARO/
├── pyproject.toml              # Installable package metadata and CLI entry point
├── main.py                     # Editable user script; edit parameters here
├── autorotorb/
│   ├── __init__.py             # Package exports
│   ├── cli.py                  # Command-line interface
│   ├── config.py               # User-facing configuration dataclasses
│   ├── models.py               # Internal result/data structures
│   ├── io_utils.py             # File-reading utilities
│   ├── parser.py               # ORCA Löwdin population parser
│   ├── selection.py            # Orbital ranking and candidate selection
│   ├── rotation.py             # Orbital swap detection and rotate block creation
│   ├── analysis.py             # Full active-space analysis pipeline
│   └── reporting.py            # Text report generation
├── tests/
│   ├── fixtures/               # Minimal ORCA snippets for automated tests
│   └── test_*.py
├── examples/
│   └── basic_usage.py          # Minimal usage example
└── data/                       # Place ORCA output files here
```

---

## ▶️ How to Use

### 1. Requirements

ARO uses only the Python standard library. Python 3.9 or newer is recommended.

```bash
python --version
```

### 2. Install (optional)

Install in editable mode to use the `aro` command from anywhere:

```bash
pip install -e .
```

### 3. Add Your ORCA Output File

Place your ORCA output file inside the `data/` folder. A tiny example ship with the repository:

```text
data/minimal_orca.out
```

The file must contain the ORCA section:

```text
LOEWDIN REDUCED ORBITAL POPULATIONS PER MO
```

### 4. Run via `main.py`

Edit `main.py`, then:

```bash
python main.py
```

### 5. Run via CLI

```bash
python -m autorotorb.cli -i data/your_job.out --active-electrons 11 \
    --orbital-request 0 Er f 7 --report data/aro_report.txt
```

After `pip install -e .`:

```bash
aro -i data/your_job.out --active-electrons 11 --orbital-request 0 Er f 7
```

Each `--orbital-request` uses four values: `LABEL SYMBOL TYPE COUNT`. Repeat the flag for mixed active spaces.

Use `--spin none` to accumulate both spin blocks.

### 6. Run Tests

```bash
python -m unittest discover -s tests -v
```

---

## 📌 Notes

* Atom labels are taken from the ORCA Löwdin table, not necessarily from the XYZ file.
* Molecular orbital indices follow the six-column layout in ORCA population tables.
* If several Löwdin tables appear in one output file, **only the last table** is used.
* `wanted_spin` can be `"SPIN UP"`, `"SPIN DOWN"`, or `None`.
* The method assumes a closed inactive orbital space when inferring the active orbital window.
* ARO raises an error if the number of orbitals to swap in and out of the active space does not match.
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
