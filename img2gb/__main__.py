import sys

from PIL import Image

from .cli import parse_cli
from .gbtileset import GBTileset
from .export import tileset_to_c, tileset_to_h


def main(argv=sys.argv):
    args = parse_cli(argv[1:])
    image = Image.open(args.image)
    tileset = GBTileset.from_image(image)
    args.c_file.write(tileset_to_c(tileset))
    if args.header_file:
        args.header_file.write(tileset_to_h(tileset))


if __name__ == "__main__":
    main()
