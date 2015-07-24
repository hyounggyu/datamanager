import argparse

from .create import start_create

def parse_args():
    parser = argparse.ArgumentParser(prog='datamanager')
    parser.add_argument('--version', help='version help')

    subparsers = parser.add_subparsers(help='sub commands')

    createqt_parser = subparsers.add_parser('create', help='createqt help')
    createqt_parser.set_defaults(func=start_create)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

parse_args()
