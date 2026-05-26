from __future__ import annotations

from config import ANALYSIS_CONFIG, REPORT_FILE

from autorotorb import analyze_active_space
from autorotorb.reporting import print_result, save_result


def main() -> None:
    result = analyze_active_space(ANALYSIS_CONFIG)
    print_result(result)
    save_result(result, REPORT_FILE)


if __name__ == "__main__":
    main()
