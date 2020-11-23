# Front Door

[![Travis Build Status](https://travis-ci.org/TimSimpson/frontdoor.svg?branch=master)](https://travis-ci.org/TimSimpson/frontdoor)
[![Build status](https://ci.appveyor.com/api/projects/status/vqcmfp6sflj902o7/branch/master?svg=true)](https://ci.appveyor.com/project/TimSimpson/frontdoor/branch/master)
[![PyPi](https://img.shields.io/pypi/v/frontdoor)](https://pypi.org/project/frontdoor)

[View change log](changelog.md)

This simple module aids in the creation of "front door" scripts, which
can help organize automated scripts and reduce the need for overly
verbose docs. The idea is you can copy `frontdoor/__init__.py` into your
repository as `frontdoor.py` to make it easy to bootstrap a front door script
of your own. The [example](example.py) files in this repo illustrate how
frontdoor.py is used).

A front door script is a command which accepts a series of options which
themselves may defer to other commands or processes which do work of
some kind.

So say you have a project that has unit tests, integration tests, and
deployment scripts. Typically you'd include a series of scripts, along
with documentation on what scripts do what and how. What makes a front
door script different is that you just document it's available and users
can find other options by jumping in and exploring it themselves. The
end result feels a little like playing an interactive fiction computer
game such as Zork.

This solves a different use case from argparse as argparse is more about
creating robust, single purpose tools that can be invoked in flexible
ways, where as Front Door is about creating scripts that more easily
accept positional arguments and can defer to other commands. It's also
extremely simple and designed to be copy and pasted.

## Example

```py3
import argparse
import os
import pathlib
import subprocess
import sys

import frontdoor


REGISTRY = frontdoor.CommandRegistry('ci')
cmd = REGISTRY.decorate


@cmd('clean', 'Destroys any build artifacts')
def clean() -> None:
    # `frontdoor` has it's own type annotations, but supports Python 2 as well
    shutil.rmtree('output')
    # If `None` is returned, then frontdoor returns zero, unless there's
    # an unhandled exception

@cmd('run', 'Runs a built program', 'Runs a program in the `output` directory')
def run(args: t.List[str]) -> int:
    # If args are passed, you need to parse them yourself
    if len(args) < 1:
        print("expected a program to run")
        return 1
    prog = pathlib.Path('output') / args[0]
    rest = args[1:]
    result = subprocess.run([prog] + rest)
    return result.returncode

@cmd('build', 'Builds a target', 'Calls the compiler')
def build(args: t.List[str]) -> None:
    # Let's assume this subcommand is complex or becomes complex. In that case
    # busting out argparse is recommended.
    parser = argparse.Parser('Builder')
    # assume more work goes into building out "parser" here, then-
    p_args = parser.parse_args(args)  # just pass `args` into argparse
    # do whatever you need with p_args


def main() -> None:
    # Fix goofy bug when using Windows command prompt to ssh into Vagrant box
    # that puts \r into the strings.
    args = [arg.strip() for arg in sys.argv[1:]]
    sys.exit(REGISTRY.dispatch(args))


if __name__ == "__main__":
    main()
```
