"""Definition of the cli argument parser."""
import argparse

from friss_matcher.definitions import DEFAULT_PORT


def get_arg_parser():
    """Initialize argument parser."""
    parser = argparse.ArgumentParser("friss-matcher")
    subparsers = parser.add_subparsers()

    # manage subparser
    parser_manage = subparsers.add_parser("manage", help="Run administrative tasks.")
    parser_manage.set_defaults(dest="manage")

    # api subparser
    parser_api = subparsers.add_parser("api", help="Run API service.")
    parser_api.set_defaults(dest="api")

    parser_api.add_argument(
        "-p",
        "--port",
        type=int,
        help="Set the port number in which this services will be listening.",
        default=DEFAULT_PORT,
        required=False,
    )

    return parser


def is_empty_namespace(namespace):
    return namespace == argparse.Namespace()
