# Hourly register

> "_Because I got tired of filling templates on Google Sheets._"
>
> -- <cite>The Author</cite>

According to Spanish Law, all paid company employees must fill a monthly form declaring, for each
working day of the given month, their arriving and leaving times.

But, instead of filling up a template, why not write a small YAML file with all necessary
information and then letting some code generate a PDF report for you?

In order to do so, we use [Jinja](https://jinja.palletsprojects.com/) in order to generate a
[LaTeX](https://www.latex-project.org/) file, which can be compiled to a PDF file using `pdflatex`.


## Setup

Before going ahead, you should have set:

- A Python 3.8, hopefully in a virtual environment.
- We use [poetry](https://python-poetry.org/) for dependency management.
- A working LaTeX distribution installed, with access to a `pdflatex` binary in your path. Most of
  the packages we use, such as `graphicx` or `kpfonts`, which should be included in most
  distributions, such as [TeX Live](https://www.tug.org/texlive/).

Once these are enabled, get the code.
```bash
$ git clone git@github.com:ber2/hourly-register.git
```
Next, get all necessary dependencies.
```bash
$ poetry install --no-dev
```
Feel free to omit the `--no-dev` flag if you wish to run any tests or use the code in a development
environment.

## Supplying data for the report

A YAML file has to be provided following the same structure of `example.yaml`, available at the repo
root, whose contents we detail below:
```yaml
# Year and month of the report
year: 2020
month: 9

dates off:
  # Label here weekdays which you take off, aka weekends.
  # Monday is 1, Sunday is 7; leave as it is for usual weekends.
  weekdays:
    - 6
    - 7

  # List of days during which you did not work, away from weekends.
  # These could be bank holidays or vacations
  holidays:
    - 11
    - 24

# Hours at which you start work, stop for lunch break, get back to work, and finish.
working hours:
  - 9
  - 13
  - 14
  - 18

# Details of the worker, aka the person filling the report.
worker:
  name: "The Guy"  # Initials will be extracted from here for signature of daily rows
  dni: "12345678A"  # National ID number

  # Social security number, to be rendered as 
  # "08 / 12345678 / 15"
  ss_n:  
    - "08"
    - "12345678"
    - "15"

# Details about your employer
company:
  name: "The Boss"  # Company name
  workplace: "Home"  # Office location
  cif: "A12345678"  # Company's fiscal number, aka as NIF

  # Código de Cuenta de Cotización, aka, a Company's social security number. To be rendered as:
  # "08 / 12345678 / 15"
  ccc:
    - "08"
    - "12345678"
    - "15"
```

### Signature

The file `signature.png`, also at the repo root, should be modified to contain a 6cm wide, 3cm tall
picture of a scanned signature.

## Report

`report.py` contains a script which will load an `example.yaml` file, render it into a TeX file,
`hourly_report.tex`, and finally generate a pdf file, `hourly_report.pdf`.

It is possible to pass optional parameters into the script specifying alternative locations
different locations for the aforementioned files, as shown below.
```bash
$ python report.py --help
Usage: report.py [OPTIONS]

  Read config file and output a PDF report

Options:
  -c, --config-file TEXT  Path to the YAML file containing necessary config.
                          Defaults to 'example.yaml'.

  -t, --template TEXT     Path to the source jinja template. Defaults to
                          'latex/template.tex'.

  -o, --output TEXT       Path for the PDF report. The same filename will be
                          used for intermediate TeX files. Defaults to
                          'hourly_report.pdf'.

  --help                  Show this message and exit.
```

