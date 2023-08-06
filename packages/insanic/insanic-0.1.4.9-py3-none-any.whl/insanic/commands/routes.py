from typing import Any

from insanic.commands import SyncCommand
from insanic.utils import load_application

class RoutesCommand(SyncCommand):
    help = 'Prints all registered routes'

    def execute(self, **kwargs: Any) -> None:
        application = load_application()

        for route in application.router.routes_all.values():
            print(route.uri)
