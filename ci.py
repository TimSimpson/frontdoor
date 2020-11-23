import argparse
import pathlib
import shutil
import subprocess
import sys
import textwrap
# `frontdoor` supports both MyPy type annotations and Python 2
import typing as t

import frontdoor


REGISTRY = frontdoor.CommandRegistry('ci')
cmd = REGISTRY.decorate


# Creates a subcommand that can be invoked using either `c` or `clean`
# The second argument is the description which is shown when frontdoor lists
# all commands.

@cmd(['c', 'clean'], 'Destroys any build artifacts')
def clean() -> None:
    # `frontdoor` has it's own type annotations, but supports Python 2 as well
    shutil.rmtree('output')
    # If `None` is returned, then frontdoor returns zero, unless there's
    # an unhandled exception


# The third arg to `cmd` can be advanced help seen when the command is passed
# to frontdoor's built in `help` command.


@cmd('run', 'Runs a built program', 'Runs a program in the `output` directory')
def run(args: t.List[str]) -> int:
    # If args are passed, you need to parse them yourself
    if len(args) < 1:
        print("expected a program to run")
        return 1
    prog = pathlib.Path('output') / args[0]
    rest = args[1:]
    result = subprocess.run([str(prog)] + rest)
    return result.returncode


@cmd('build', 'Builds a target', 'Calls the compiler')
def build(args: t.List[str]) -> None:
    # Let's assume this subcommand is complex or becomes complex. In that case
    # busting out argparse is recommended.
    parser = argparse.ArgumentParser('Builder')
    # assume more work goes into building out "parser" here, then-
    p_args = parser.parse_args(args)  # just pass `args` into argparse  # NOQA
    # do whatever you need with p_args


# While frontdoor automatically adds a `help` command, you can override it
# if you want.
@cmd("help", desc="What's all this about?",
     help="Whoa. You want to see help about the help itself?\n"
          "... I don't know what to do. I feel so lost.")
def help(args: t.List[str]) -> None:
    print(
        textwrap.dedent(
            """
         Root CI script for project
        """
        )
    )
    # Then just use frontdoor's default help mechanism
    REGISTRY.help(args)


def main() -> None:
    # Fix goofy bug when using Windows command prompt to ssh into Vagrant box
    # that puts \r into the strings.
    args = [arg.strip() for arg in sys.argv[1:]]
    sys.exit(REGISTRY.dispatch(args))


if __name__ == "__main__":
    main()
