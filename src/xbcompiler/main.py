"""Entry-point for XB Compiler application"""

import argparse

from loguru import logger

logger.disable("xbcompiler")


def main(file: bytes) -> bytes:
    """Compile a given XLA file"""
    logger.debug("Starting the compiling process, given bytes")

    return b"hi"


def run_cli() -> int:
    """Run the compiler as CLI app"""

    parser = argparse.ArgumentParser(
        description="Xilia Base Compiler (XLA => LUA)")
    parser.add_argument("file", type=str, nargs=1,
                        help="path to XLA file to compile")
    parser.add_argument("-o", metavar="output", type=str,
                        nargs="?", help="where to output the result")

    args = parser.parse_args()
    file_path = args.file[0]
    output_path = "xbcompiler-out.zip" if args.o is None else args.o

    with open(file_path, "rb") as file:
        contents = file.read()
        result = main(contents)

    logger.debug("Writing compiler result to output file..")
    with open(output_path, "wb") as file:
        file.write(result)

    return 0

    # except FileNotFoundError:
    #     print(f"Error: file {file_path} not found!")
    #     return 1


if __name__ == "__main__":
    logger.trace("Running XBCompiler as a CLI application..")
    run_cli()
