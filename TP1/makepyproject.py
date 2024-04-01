#!/usr/bin/env python3
"""python makepyproject.py"""

import jinja2
import jjcli
from glob import glob
import os
import json

def main():
    #project name
    modes = glob("*.py")
    if len(modes)==1:
        name = modes[0].replace(".py","")
    elif len(modes)>1:
        print(modes)
        name = input("Modulo?").replace(".py","")
    else:
        name = input("Modulo?").replace(".py","")

    v = jjcli.qx(f"grep name '{name}.py'")
    print("Debug: ", len(v))

    version = "0.0.1"

    # Create Jinja2 template
    pp = jinja2.Template("""[build-system]
    requires = ["flit_core >=3.2,<4"]
    build-backend = "flit_core.buildapi"

    [project]
    name = "{{name}}"
    authors = [
        {% for author in authors %}
        {name = "{{author.name}}", email = "{{author.email}}"},
        {% endfor %}
    ]
    version = "{{version}}"
    classifiers = [
        "License :: OSI Approved :: MIT License",
    ]
    requires-python = ">=3.8"
    dynamic = ["description"]
    dependencies = [
        "jjcli","spacy"
    ]

    [project.scripts]
    {{name}} = "{{name}}:main"
    """)

    authors = [
        {'name': 'Vasco Oliveira', 'email': 'pg54269@alunos.uminho.pt'},
        {'name': 'João Loureiro', 'email': 'pg53924@alunos.uminho.pt'},
        {'name': 'Luís Fernandes', 'email': 'pg54019@alunos.uminho.pt'}
    ]

    out = pp.render({"name": name, "authors": authors, "version": version})
    print("Debug: ", out)

    file_output = open("pyproject.toml", "w")
    file_output.write(out)

if __name__ == "__main__":
    main()