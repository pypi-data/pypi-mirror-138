# -*- coding: utf-8 -*-

import sys

from wilderness import Application
from wilderness import Command

from veld.__version__ import __version__

from .commands.count import CountCommand
from .commands.max import MaxCommand
from .commands.mean import MeanCommand
from .commands.min import MinCommand
from .commands.mode import ModeCommand
from .commands.sum import SumCommand


class VeldApplication(Application):
    def __init__(self):
        super().__init__(
            "veld",
            version=__version__,
            title="easy command line statistics",
            author="Gerrit J.J. van den Burg",
        )

    def register(self):
        self.add_argument(
            "-V",
            "--version",
            help="show version information and exit",
            action="version",
            version=__version__,
        )
        self.add_argument(
            "--debug",
            help="Enable debug mode",
            action="store_true",
            description=(
                "Debug mode disables the default exception handling, which "
                "can be useful for debugging."
            ),
        )

    def set_excepthook(self) -> None:
        sys_hook = sys.excepthook

        def exception_handler(exception_type, value, traceback):
            if self.args.debug:
                sys_hook(exception_type, value, traceback)
            else:
                print(value, file=sys.stderr)

        sys.excepthook = exception_handler

    def run_command(self, command: Command) -> int:
        self.set_excepthook()
        return super().run_command(command)


def build_application() -> Application:
    app = VeldApplication()
    app.set_prolog("Below are the available Veld commands")

    group = app.add_group("extreme values and counts")
    group.add(MinCommand())
    group.add(MaxCommand())
    group.add(CountCommand())

    group = app.add_group("univariate statistics")
    group.add(SumCommand())
    group.add(MeanCommand())
    group.add(ModeCommand())

    # group = app.add_group("hypothesis testing")
    # group.add(PairedTTestCommand())

    # group = app.add_group("plotting")
    # group.add(LinePlotCommand())
    # group.add(ScatterPlotCommand())
    # group.add(HistogramCommand())
    return app
