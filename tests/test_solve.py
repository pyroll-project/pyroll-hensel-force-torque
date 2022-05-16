from pathlib import Path

from pyroll.core import solve
from pyroll.ui import Exporter, Reporter


def test_solve(tmp_path: Path):
    import pyroll.ui.cli.res.input_trio as input_py
    import pyroll.hensel_force

    sequence = input_py.sequence

    solve(sequence, input_py.in_profile)
    print()

    rendered = Reporter().render(sequence)
    report_file = tmp_path / "report.html"
    report_file.write_text(rendered)
    print(report_file)

    exported = Exporter().export(sequence, "csv")
    export_file = tmp_path / "export.csv"
    export_file.write_bytes(exported)
    print(export_file)
