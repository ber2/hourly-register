import os
from pathlib import Path

from pytest import mark

from src.render import render


@mark.xfail
def test_render_latex_template(hourly_config):

    template_path = Path("latex/template.tex")
    actual_path = Path("tests/actual_rendered_template.tex")

    # TODO Remove these lines after test passes
    if os.path.exists(actual_path):
        os.remove(actual_path)

    expected_path = Path("tests/expected_rendered_template.tex")

    render(hourly_config, template_path, actual_path)

    with open(actual_path, "r") as f:
        actual = f.read()

    with open(expected_path, "r") as f:
        expected = f.read()

    assert actual == expected

    # TODO Uncomment below after passing test; use it for diffs
    # os.remove(actual_path)
