# -*- coding: utf-8 -*-

"""Base command for all Veld commands

"""

from wilderness import Command


class BaseCommand(Command):
    def register(self):
        self.add_argument(
            "-e",
            "--encoding",
            help="Encoding if the input stream",
            default="utf-8",
            description=("Specify the encoding of the input stream."),
        )
        self.add_argument(
            "-f",
            "--flatten",
            help="Apply operation on flattened input",
            action="store_true",
            description=(
                "With multidimensional input (more than one value per line) "
                "the operation is conducted on each dimension independently. "
                "With the --flatten option, the input is considered to be a "
                "one-dimensional array and the operation is conducted on all "
                "input values together."
            ),
        )
        self.add_argument(
            "-i",
            "--ignore",
            help="Ignore non-numeric values in the input stream",
            action="store_true",
        )
        self.add_argument(
            "-s",
            "--separator",
            help="Separator for values in the stream",
            description=(
                "Some of the Veld commands have support for "
                "multidimensional input data. The values on each line "
                "of the input stream are expected to be separated by this "
                "separator. If omitted, input data will be split on "
                "any whitespace."
            ),
        )
        self.add_argument(
            "file",
            help="File to read from (otherwise stdin)",
            nargs="?",
            description=(
                "Veld is primarily designed for processing input streams, "
                "but it can also be applied on a file of data, which can "
                "be supplied with this argument. By default Veld will read "
                "the input data from stdin."
            ),
        )
