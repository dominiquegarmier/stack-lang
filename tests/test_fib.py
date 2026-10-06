from __future__ import annotations

from pathlib import Path

from stack.__main__ import run

FIB_PATH = Path(__file__).parent.parent / "examples/fib.s"


def test_fib(capsys):
    with open(FIB_PATH) as f:
        run(f)

    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "<LITERAL 4181>\n"
