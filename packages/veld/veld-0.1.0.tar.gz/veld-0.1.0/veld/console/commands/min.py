# -*- coding: utf-8 -*-

import math

from veld.stream_processor import StreamProcessor

from .base import BaseCommand


class MinCommand(BaseCommand):
    def __init__(self):
        super().__init__(
            name="min",
            title="Find the minimum ofthe values in the data stream",
        )

    def register(self):
        super().register()

    def handle(self) -> int:
        sp = StreamProcessor(
            path=self.args.file,
            sep=self.args.separator,
            encoding=self.args.encoding,
            flatten=self.args.flatten,
            ignore_invalid=self.args.ignore,
        )
        mins = None
        for values in sp:
            if mins is None:
                mins = [float("inf")] * len(values)

            for i in range(len(values)):
                val = values[i]
                if math.isnan(val):
                    continue
                mins[i] = min(mins[i], val)
        print(" ".join(map(str, mins)))
        return 0
