from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .config_loader import ReportData


def render(data: ReportData, template_path: Path, output_path: Path) -> None:

    loader = FileSystemLoader(template_path.parent)
    env = Environment(loader=loader)

    template = env.get_template(template_path.name)
    rendered_output = template.render(data=data)

    with open(output_path, "w") as f:
        f.write(rendered_output)
