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
            alternative_palette=args.alternative_palette,
            sprite8x16=args.sprite8x16,
        )
    elif args.subcommand == "tilemap":
        tileset = Image.open(args.tileset)
        tilemap = Image.open(args.tilemap)
        generate_tilemap(
            tileset,
            tilemap,
            output_c=args.output_c_file,
            output_h=args.output_header_file,
            name=args.name,
            offset=args.offset,
            missing=args.missing,
            replace=args.replace,
        )


if __name__ == "__main__":
    main()
