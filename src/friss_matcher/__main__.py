# -*- coding: utf-8 -*-
"""Launch friss-matcher tool via python -m."""

import os
import sys

import uvicorn

from friss_matcher.asgi import application
from friss_matcher.cli import get_arg_parser, is_empty_namespace


def manage(argv):
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friss_matcher.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(argv)


def main():
    """Main entry point for this project."""
    cli_parser = get_arg_parser()

    cli_args, unknown_cli_args = cli_parser.parse_known_args()

    if is_empty_namespace(cli_args):
        cli_parser.print_help(sys.stderr)
        sys.exit(1)

    if cli_args.dest == "api":
        uvicorn.run(application, host="0.0.0.0", port=cli_args.port)

    elif cli_args.dest == "manage":
        args = ["friss_matcher"]
        args.extend(unknown_cli_args)
        manage(args)


if __name__ == "__main__":
    main()
