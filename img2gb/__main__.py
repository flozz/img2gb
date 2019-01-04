import sys

from PIL import Image

from .cli import parse_cli
from . import generate_tileset, generate_tilemap


def main(argv=sys.argv):
    args = parse_cli(argv[1:])

    if args.subcommand == "tileset":
        images = [Image.open(image) for image in args.image]
        generate_tileset(
                images,
                output_c=args.output_c_file,
                output_h=args.output_header_file,
                output_image=args.output_image,
                name=args.name,
                dedup=args.deduplicate,
                alternative_palette=args.alternative_palette
                )
    else:
        raise NotImplementedError()
    # image = Image.open(args.image)
    # tilemap = GBTilemap.from_image(image, dedup=args.deduplicate)
    # tileset = tilemap.tileset
    # if not args.map:
        # tilemap = None
    # args.c_file.write(tileset_to_c(tileset, tilemap, name=args.name))
    # if args.header_file:
        # args.header_file.write(tileset_to_h(tileset, tilemap, name=args.name))


if __name__ == "__main__":
    main()
