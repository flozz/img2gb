import argparse


def generate_tileset_cli(parser):
    # Positional
    parser.add_argument(
            "image",
            type=argparse.FileType("rb"),
            nargs="+",
            help="input image file"
            )
    # Options
    parser.add_argument(
            "-c",
            "--output-c-file",
            type=argparse.FileType("w"),
            metavar="FILE",
            help="output C file"
            )
    parser.add_argument(
            "-H",
            "--output-header-file",
            type=argparse.FileType("w"),
            metavar="FILE",
            help="output C header file"
            )
    parser.add_argument(
            "-i",
            "--output-image",
            type=argparse.FileType("wb"),
            metavar="FILE",
            help="output image file representing the tileset (required to generate a tilemap)"  # noqa
            )
    parser.add_argument(
            "-d",
            "--deduplicate",
            action="store_true",
            default=False,
            help="remove duplicated tiles from the tileset"
            )
    parser.add_argument(
            "-a",
            "--alternative-palette",
            action="store_true",
            default=False,
            help="invert the colors to allow tiles to be used with the sprites alternative palette"  # noqa
            )
    parser.add_argument(
            "-n",
            "--name",
            type=str,
            default="TILESET",
            help="name of the tileset (used for variable names in generated code, default=TILESET)"  # noqa
            )


def generate_tilemap_cli(parser):
    # Positional
    parser.add_argument(
            "tileset",
            type=argparse.FileType("rb"),
            help="the tileset (generated by img2gb tileset -i)"
            )
    parser.add_argument(
            "tilemap",
            type=argparse.FileType("rb"),
            help="an image representing the tilemap"
            )
    # Options
    parser.add_argument(
            "-c",
            "--output-c-file",
            type=argparse.FileType("w"),
            metavar="FILE",
            help="output C file"
            )
    parser.add_argument(
            "-H",
            "--output-header-file",
            type=argparse.FileType("w"),
            metavar="FILE",
            help="output C header file"
            )

    parser.add_argument(
            "-o",
            "--offset",
            type=int,
            help="offset of the tileset in the video memory (default = 0)"
            )
    parser.add_argument(
            "-m",
            "--missing",
            choices=["error", "replace"],
            help="action to do when a tile of the tilemap is missing from the tileset (default = error)"  # noqa
            )
    parser.add_argument(
            "-r",
            "--replace",
            type=int,
            metavar="TILE_ID",
            help="replace missing tiles by the given one when --missing=replace"  # noqa
            )
    parser.add_argument(
            "-n",
            "--name",
            type=str,
            default="TILEMAP",
            help="name of the tileset (used for variable names in generated code, default=TILEMAP)"  # noqa
            )


def generate_cli():
    parser = argparse.ArgumentParser(
            prog="img2gb",
            description="Converts images to GameBoy tilesets and tilemaps"
            )
    subparsers = parser.add_subparsers(dest="subcommand")

    tileset_parser = subparsers.add_parser(
            "tileset",
            help="Generates GameBoy tilesets"
            )
    generate_tileset_cli(tileset_parser)

    tilemap_parser = subparsers.add_parser(
            "tilemap",
            help="Generates GameBoy tilemaps"
            )
    generate_tilemap_cli(tilemap_parser)

    return parser


def parse_cli(args):
    parser = generate_cli()
    return parser.parse_args(args)
