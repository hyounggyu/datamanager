import argparse
from pathlib import Path

def _findtiff(path, prefix):
    return [p for p in path.iterdir() if p.match(prefix.strip()+'*') and (p.suffix.lower() in ['.tif', '.tiff'])]

def new_dataset(args):
    from xni import dataset
    path = Path(args.path)
    images = _findtiff(path, args.image_prefix)
    bgnds = _findtiff(path, args.background_prefix) if args.background_prefix != None else []
    darks = _findtiff(path, args.dark_prefix) if args.dark_prefix != None else []
    images = [str(im) for im in images]
    bgnds = [str(im) for im in bgnds]
    darks = [str(im) for im in darks]
    nw = dataset.new(args.output, images, bgnds, darks)
    for i, p in nw:
        print(p)

parser = argparse.ArgumentParser(prog='datamanager')
subparsers = parser.add_subparsers(help='sub commands')

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
