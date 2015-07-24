import argparse

from .create import start_create, start_createqt
from .view import start_view, start_remoteview

def parse_args():
    parser = argparse.ArgumentParser(prog='datamanager')
    parser.add_argument('--version', help='version help')

    subparsers = parser.add_subparsers(help='sub commands')

    createqt_parser = subparsers.add_parser('createqt', help='createqt help')
    createqt_parser.set_defaults(func=start_createqt)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

parse_args()
