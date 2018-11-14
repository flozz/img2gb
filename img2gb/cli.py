import argparse


def parse_cli(args):
    parser = argparse.ArgumentParser(
            prog="img2gb",
            description="Converts images to GameBoy tiles"
            )
    parser.add_argument(
            "image",
            type=argparse.FileType("rb"),
            help="Input image file"
            )
    parser.add_argument(
            "c_file",
            type=argparse.FileType("w"),
            help="Ouput C File",
            )
    parser.add_argument(
            "-H",
            "--header-file",
            type=argparse.FileType("w"),
            default=None,
            help="Output file for C Header (.h)"
            )
    parser.add_argument(
            "-m",
            "--map",
            action="store_true",
            default=False,
            help="Add tilemap to the .c / .h files"
            )
    parser.add_argument(
            "-d",
            "--deduplicate",
            action="store_true",
            default=False,
            help="Remove duplicated tiles from the tileset"
            )
    parser.add_argument(
            "-n",
            "--name",
            type=str,
            default="TILESET",
            help="Name of the tileset (used for variable names in generated code, default=TILESET)"  # noqa
            )
    return parser.parse_args(args)
