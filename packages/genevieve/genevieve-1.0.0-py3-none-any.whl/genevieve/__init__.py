"""
Generates `env.env` on Linux and `env.ps1` on Windows.

Since child subprocess cannot set exported environment variables,
this script is used to generate shell scripts that can be sourced
for Windows and Linux.
"""

__version__ = "1.0.0"

import argparse
from os import PathLike
from typing import Any, Callable, Dict, Union
import yaml


def assert_key_exists(parsed_yaml: Dict[str, Any], key: str):
    if key not in parsed_yaml.keys():
        raise KeyError(key)


# TODO: allow platform-scoped variables!!
# e.g. `windows`, `linux`, `macos` keys at the same level as `variables`
def generate_sh(parsed_yaml: Dict[str, Any], query_key: str) -> str:
    variables = parsed_yaml[query_key]
    str_sh = ""
    for key, value in variables.items():
        str_sh += f"export {key}=\"{value}\"\n"
    return str_sh


def generate_pwsh(parsed_yaml: Dict[str, Any], query_key: str) -> str:
    variables = parsed_yaml[query_key]
    str_pwsh = ""
    for key, value in variables.items():
        str_pwsh += f"$env:{key} = \"{value}\"\n"
    return str_pwsh


def parse_yaml(path: Union[str, PathLike]) -> Dict[str, Any]:
    with open(path, "r") as f:
        parsed_yaml = yaml.safe_load(f)
    return parsed_yaml


def main(printer: Callable):
    def _main():
        parser = argparse.ArgumentParser(description="Generates env.env and env.ps1")
        parser.add_argument("-f", "--file",
                            help="Input YAML file", required=True)
        parser.add_argument("-o", "--output",
                            help="Output filename (without extension)")
        parser.add_argument("-d", "--debug",
                            help="Debug mode, prints to stdout instead", action="store_true")

        args = parser.parse_args()

        parsed_yaml = parse_yaml(args.file)

        variables_query_key = "variables"
        assert_key_exists(parsed_yaml, variables_query_key)

        str_sh = generate_sh(parsed_yaml, variables_query_key)
        str_pwsh = generate_pwsh(parsed_yaml, variables_query_key)

        filename = args.output or "env"

        if args.debug:
            printer(str_sh)
            printer(str_pwsh)
            exit(0)

        with open(f"{filename}.sh", "w") as f:
            f.write(str_sh)

        with open(f"{filename}.ps1", "w") as f:
            f.write(str_pwsh)
    return _main


if __name__ == "__main__":
    main(print)
