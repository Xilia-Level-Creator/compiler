"""Entry-point for XB Compiler application"""

import argparse
import tarfile
import gzip
import io

from loguru import logger
import magic

from parser.main import parse

logger = logger.opt(colors=True)
logger.disable("xbcompiler")


def uncompress_tarball(file: bytes) -> bytes:
    """Uncompress gzip-compressed tarball"""
    logger.debug("Uncompressing gzip-compressed tarball")

    tarball = gzip.decompress(file)

    # [TODO: take only the start of big files]
    file_type = magic.from_buffer(tarball, mime=True)

    logger.debug("Detected file (mime) type to be <m>{}</>", file_type)

    if file_type != "application/x-tar":
        raise ValueError(
            f"Invalid file type (after gzip decompressing): {file_type}"
        )

    return tarball


def main(file: bytes) -> bytes:
    """Compile a given XLA file"""
    logger.debug("Starting the compiling process, given bytes")

    # [TODO: take only the start of big files]
    file_type = magic.from_buffer(file, mime=True)

    logger.debug("Detected file (mime) type to be <m>{}</>", file_type)

    if file_type == "application/gzip":
        # tarball = uncompress_tarball(file)
        io_bytes = io.BytesIO(file)
        tar = tarfile.open(fileobj=io_bytes, mode="r:gz")

    elif file_type == "application/x-tar":
        # tarball = file
        io_bytes = io.BytesIO(file)
        tar = tarfile.open(fileobj=io_bytes, mode="r")

    else:
        raise ValueError(f"Invalid file type given: {file_type}")

    logger.trace("Successfully got tar data from XLA")

    files = map(tar.extractfile, tar.getmembers())
    result = parse([x for x in files if x is not None])

    return bytes(result, encoding="UTF-8")


def run_cli() -> int:
    """Run the compiler as CLI app"""

    logger.remove()

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
