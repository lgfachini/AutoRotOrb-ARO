from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional

from . import __version__
from .analysis import analyze_active_space
from .config import AnalysisConfig, OrbitalRequest
from .reporting import print_result, save_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aro",
        description=(
            "AutoRotOrb (ARO): analyze ORCA Loewdin populations and "
            "suggest active-space orbital rotations."
        ),
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=Path,
        help="ORCA output file to analyze.",
    )
    parser.add_argument(
        "--active-electrons",
        required=True,
        type=positive_int,
        help="Number of active electrons in the intended active space.",
    )
    parser.add_argument(
        "--orbital-request",
        nargs=4,
        action="append",
        metavar=("LABEL", "SYMBOL", "TYPE", "COUNT"),
        required=True,
        help=(
            "Atom/orbital selection: label symbol shell count. "
            "Repeat for multiple requests."
        ),
    )
    parser.add_argument(
        "--spin",
        default="SPIN UP",
        help='Spin block: "SPIN UP", "SPIN DOWN", or "none" for all spins.',
    )
    parser.add_argument(
        "--max-orbital-index",
        type=non_negative_int,
        default=None,
        help="Upper MO index for candidates (default: active-space end).",
    )
    parser.add_argument(
        "--round-digits",
        type=non_negative_int,
        default=1,
        help="Decimal places when ranking populations.",
    )
    parser.add_argument(
        "--rotation-angle",
        type=non_zero_int,
        default=90,
        help="Rotation angle for generated ORCA rotate commands.",
    )
    parser.add_argument(
        "-o",
        "--report",
        type=Path,
        default=None,
        help="Optional path to save a text report.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def parse_spin_argument(spin: str) -> Optional[str]:
    if spin.strip().lower() in {"none", "all"}:
        return None
    return spin


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer.") from exc

    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be a positive integer.")

    return parsed


def non_negative_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer.") from exc

    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be zero or greater.")

    return parsed


def non_zero_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer.") from exc

    if parsed == 0:
        raise argparse.ArgumentTypeError("value must be non-zero.")

    return parsed


def orbital_requests_from_args(
    raw_requests: List[List[str]],
) -> List[OrbitalRequest]:
    requests: List[OrbitalRequest] = []
    for label, symbol, orbital_type, count in raw_requests:
        requests.append(
            OrbitalRequest(
                atom_label=label,
                atom_symbol=symbol,
                orbital_type=orbital_type,
                number=positive_int(count),
            )
        )
    return requests


def config_from_args(args: argparse.Namespace) -> AnalysisConfig:
    return AnalysisConfig(
        output_file=args.input,
        orbital_requests=orbital_requests_from_args(args.orbital_request),
        active_electrons=args.active_electrons,
        wanted_spin=parse_spin_argument(args.spin),
        max_orbital_index=args.max_orbital_index,
        population_round_digits=args.round_digits,
        rotation_angle=args.rotation_angle,
    )


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        config = config_from_args(args)
        result = analyze_active_space(config)
        print_result(result)
        save_result(result, args.report)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"{parser.prog}: error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
