import logging
import sys
from argparse import ArgumentParser
from typing import Any

class Command:
    help: str | None = None
    parser: ArgumentParser = ArgumentParser()

    def exit(self, exit_code: int = 0):  # pylint: disable=no-self-use
        sys.exit(exit_code)

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def execute(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()
