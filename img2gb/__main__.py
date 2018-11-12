import sys

from PIL import Image

from .cli import parse_cli
from .gbtilemap import GBTilemap
from .export import tileset_to_c, tileset_to_h


def main(argv=sys.argv):
    args = parse_cli(argv[1:])
    image = Image.open(args.image)
    tilemap = GBTilemap.from_image(image)
    tileset = tilemap.tileset
    if not args.map:
        tilemap = None
    args.c_file.write(tileset_to_c(tileset, tilemap))
    if args.header_file:
        args.header_file.write(tileset_to_h(tileset, tilemap))


if __name__ == "__main__":
    main()
