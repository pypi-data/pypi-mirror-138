from importlib import import_module
from argparse import ArgumentParser
from dfrost.lib.log import info
from dfrost.lib.command import get_command_registry

import_module("dfrost.pull")
import_module("dfrost.push")
import_module("dfrost.generate")


def run():
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="_command")
    subparsers.required = True
    for name, (setup_fn, _command_fn) in get_command_registry().items():
        setup_fn(subparsers.add_parser(name))

    args = parser.parse_args()
    info(f"Invoked: {args._command}")
    get_command_registry()[args._command][1](args)


if __name__ == "__main__":
    run()
