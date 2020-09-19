import os
from pathlib import Path

from pytest import mark

from src.render import render


def test_render_latex_template(report_data):

    template_path = Path("latex/template.tex")
    actual_path = Path("tests/actual_rendered_template.tex")

    expected_path = Path("tests/expected_rendered_template.tex")

    render(report_data, template_path, actual_path)

    with open(actual_path, "r") as f:
        actual = f.read()

    with open(expected_path, "r") as f:
        expected = f.read()

    assert actual == expected

    os.remove(actual_path)
