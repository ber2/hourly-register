import os
from pathlib import Path

import click

from parser import load_config, render


@click.command(help="Read config file and output a PDF report")
@click.option("--config-file", "-c", default="example.yaml", help="Path to the YAML file containing necessary config.")
@click.option("--template", "-t", default="latex/template.tex",
              help="Path to the source LaTeX template that will be used for generating the PDF output")
@click.option("--output", "-o", default="hourly_report.pdf",
             help="Path for the PDF report. The same filename will be used for intermediate TeX files")
def main(config_file: str, template: str, output: str) -> None:

    config_path = Path(config_file)
    template = Path(template)
    output_pdf_path = Path(output)
    output_tex_path = Path(output_pdf_path.stem + ".tex")

    print(f"Loading data from {config_path}.")
    data = load_config(config_path)

    print(f"Rendering TeX file using template {template} and writing to {output_tex_path}.")
    render(data, template, output_tex_path)

    print(f"Running pdflatex and saving to {output_pdf_path}.")
    os.system(f"pdflatex --interaction nonstopmode {output_tex_path}")

    print("All done.")


if __name__ == "__main__":
    main()
