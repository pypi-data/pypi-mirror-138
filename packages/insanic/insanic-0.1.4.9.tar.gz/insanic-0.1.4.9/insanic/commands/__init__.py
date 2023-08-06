import logging
import sys
from argparse import ArgumentParser
from typing import Any

from insanic.utils import application_context

class CommandParser(ArgumentParser):
    pass

class Command:
    help: str | None = None
    parser: CommandParser = CommandParser()

    def exit(self, exit_code: int = 0) -> None:  # pylint: disable=no-self-use
        sys.exit(exit_code)

    def add_arguments(self, parser: CommandParser) -> None:
        pass

    async def execute_with_context(self, **kwargs: Any) -> None:
        raise NotImplementedError()

class SyncCommand(Command):
    async def execute_with_context(self, **kwargs: Any) -> None:
        self.execute(**kwargs)

    def execute(self, **kwargs: Any) -> None:
        raise NotImplementedError()

class AsyncCommand(Command):
    async def execute_with_context(self, **kwargs: Any) -> None:
        async with application_context():
            await self.execute(**kwargs)

    async def execute(self, **kwargs: Any) -> None:
        raise NotImplementedError()
