# -*- coding: utf-8 -*-

import math

from veld.stream_processor import StreamProcessor

from .base import BaseCommand


class MaxCommand(BaseCommand):
    def __init__(self):
        super().__init__(
            name="max",
            title="Find the maximum of the values in the data stream",
        )

    def handle(self) -> int:
        sp = StreamProcessor(
            path=self.args.file,
            sep=self.args.separator,
            encoding=self.args.encoding,
            flatten=self.args.flatten,
            ignore_invalid=self.args.ignore,
        )
        maxs = None
        for values in sp:
            if maxs is None:
                maxs = [-float("inf")] * len(values)

            for i in range(len(values)):
                val = values[i]
                if math.isnan(val):
                    continue
                maxs[i] = max(maxs[i], val)
        print(" ".join(map(str, maxs)))
        return 0
