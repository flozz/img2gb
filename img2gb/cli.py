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
    return parser.parse_args(args)
