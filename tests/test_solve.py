from pathlib import Path

from pyroll import solve
from pyroll.ui.exporter import Exporter
from pyroll.ui.report import Report


def test_solve(tmp_path: Path):
    import pyroll.ui.cli.res.input_trio as input_py
    import pyroll_hensel_force

    sequence = input_py.sequence

    solve(sequence, input_py.in_profile)
    print()

    rendered = Report().render(sequence)
    report_file = tmp_path / "report.html"
    report_file.write_text(rendered)
    print(report_file)

    exported = Exporter().export(sequence, "csv")
    export_file = tmp_path / "export.csv"
    export_file.write_bytes(exported)
    print(export_file)
