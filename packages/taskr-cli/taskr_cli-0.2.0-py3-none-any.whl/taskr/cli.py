import argparse
import sys

from .__version__ import version as VERSION
from .taskr import _Taskr


def main(args=None):
    parser = argparse.ArgumentParser(
        prog="taskr", description="A small utility to run tasks"
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="Show the version number"
    )
    parser.add_argument("-l", "--list", action="store_true", help="Show defined tasks")
    parser.add_argument(
        "-i",
        "--init",
        action="store_true",
        default=False,
        help="Generate a template task file",
    )

    args, custom_args = parser.parse_known_args()

    if args.init:
        _Taskr.init()
        return

    if args.version:
        print(f"Running {VERSION}")
        return

    # Below actions needs an instance of taskr

    try:
        import tasks
    except ImportError:
        print("No valid tasks.py file found in current directory. Run 'taskr --init'")
        parser.print_help()
        sys.exit(1)

    Runner = _Taskr(tasks)

    # Custom arguments take precedence
    if custom_args:
        # Custom task was passed, take it in
        task = custom_args.pop(0)
        # Ignore anything that looks like a normal arg, it shouldn't be here
        if task.startswith("-"):
            parser.print_help()
        else:
            # At this point, custom the target command, tasks are arguments for custom
            Runner.process(task, custom_args)

    # Start other commands
    elif args.list:
        Runner.list()

    # No tasks passed, check if we have a default task
    elif Runner.hasDefault():
        Runner.default()

    # Finally print help
    else:
        parser.print_help()
