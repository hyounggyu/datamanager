import argparse
from pathlib import Path


def _findtiff(path, prefix):
    return sorted([p for p in path.iterdir() if p.match(prefix.strip()+'*') and (p.suffix.lower() in ['.tif', '.tiff'])])

def new_dataset(args):
    from xni.io import dataset
    path = Path(args.path)
    images = _findtiff(path, args.image_prefix)
    bgnds = _findtiff(path, args.background_prefix) if args.background_prefix != None else []
    darks = _findtiff(path, args.dark_prefix) if args.dark_prefix != None else []
    images = [str(im) for im in images]
    bgnds = [str(im) for im in bgnds]
    darks = [str(im) for im in darks]
    for i, p in dataset.new(args.output, images, bgnds, darks):
        print(p)

def run_qt(args):
    import sys
    from .gui import App
    app = App(sys.argv)
    sys.exit(app.exec_())

def parse_args():
    parser = argparse.ArgumentParser(prog='datamanager')
    parser.add_argument('--gui', help='gui help', action='store_true')
    parser.add_argument('--version', help='version help')
    parser.set_defaults(gui=True)

    subparsers = parser.add_subparsers(help='sub commands')

    gui_parser = subparsers.add_parser('gui', help='gui help')
    gui_parser.set_defaults(func=run_qt)

    new_parser = subparsers.add_parser('new', help='new help')
    new_parser.add_argument('path', help='path help')
    new_parser.add_argument('-o', '--output', help='output help')
    new_parser.add_argument('-i', '--image-prefix', help='image prefix help')
    new_parser.add_argument('-b', '--background-prefix', help='background image prefix help', required=False)
    new_parser.add_argument('-d', '--dark-prefix', help='dark image prefix help', required=False)
    new_parser.set_defaults(func=new_dataset)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

parse_args()
