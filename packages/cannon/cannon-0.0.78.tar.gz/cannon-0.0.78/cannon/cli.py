from argparse import ArgumentParser
import sys
import os

from loguru import logger

# https://dev.to/bowmanjd/build-command-line-tools-with-python-poetry-4mnc

@logger.catch(default=True, onerror=lambda _: sys.exit(1))
def parse_args(input_str=""):
    parser = ArgumentParser(
        prog=os.path.basename(__file__),
        description="Help string placeholder",
        add_help=True,
    )

    args = parser.parse_args()
    return args

@logger.catch(default=True, onerror=lambda _: sys.exit(1))
def cli(args=None):
    pass
