import argparse
import os
import subprocess
import sys

import frontdoor

if False:
    import typing as t  # This is a well known mypy python 2 trick


REGISTRY = frontdoor.CommandRegistry('fd-ci')
cmd = REGISTRY.decorate


@cmd('list-files', 'Lists files in a directory.',
     'Calls `ls` or `dir` depending on platform.')
def list_files(args):
    # type: (t.List[str]) -> None
    if os.name == 'nt':
        cmd = 'dir'
    else:
        cmd = 'ls'
    new_args = [cmd] + args
    subprocess.check_call(' '.join(new_args), shell=True)


@cmd('calc', 'Does arithmetic on two numbers.',
     'Shows how to defer to a more complicated thing.')
def calc(args):
    # type: (t.List[str]) -> None
    parser = argparse.ArgumentParser(prog='calc',
                                     description='Does something complicated.')
    parser.add_argument('-x', type=int, help='First operand', required=True)
    parser.add_argument('--op', type=str, help='What to do.', default='+')
    parser.add_argument('-y', type=int, help='Second operand', required=True)

    ap_args = parser.parse_args(args=args)
    ops = {
        '+': lambda x, y: x + y,
        '*': lambda x, y: x * y
    }
    print("RESULT={}".format(ops[ap_args.op](ap_args.x, ap_args.y)))  # type: ignore


@cmd('hello', 'Says hello. Notice this takes no args.')
def hello():
    # type: () -> None
    print("hi!")


@cmd('subproject', 'Invokes a whole other front door module.',
     'Gives an example of how easy it is to nest front door modules. '
     'In real life it can be very useful to nest multi-project repositories '
     'this way.')
def subproject(args):
    # type: (t.List[str]) -> int
    # It may be worthwhile to put the import here to avoid paying the
    # initialization cost for all other invocations of the script.
    import subproject
    # dispatch takes the first argument off the list automatically, so there's
    # no need to muck with it.
    return subproject.REGISTRY.dispatch(args)


@cmd('help', "What's all this about?")
def help(args):
    # type: (t.List[str]) -> None
    # The CommandRegistry class already defines a version of `help`
    # which also calls the `help` method but as this shows it's possible to
    # override it. Here doing so let's us print out the text from the README,
    # which is a bit nicer since the default help only lists commands (which
    # also happens if a user mistypes a command).
    REGISTRY.help(args)
    if len(args) == 0:
        print()
        with open(frontdoor.from_root('README.md'), 'r') as file:
            print(file.read())


if __name__ == "__main__":
    # Fix goofy bug when using Windows command prompt to ssh into Vagrant box
    # that puts \r into the strings.
    args = [arg.strip() for arg in sys.argv[1:]]
    result = REGISTRY.dispatch(args)
    sys.exit(result)
