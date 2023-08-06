# -*- coding: utf-8 -*-

import math

from veld.stream_processor import StreamProcessor

from .base import BaseCommand


class MeanCommand(BaseCommand):
    def __init__(self):
        super().__init__(
            name="mean",
            title="Find the mean (average) of the values in the data stream",
        )

    def handle(self) -> int:
        sp = StreamProcessor(
            path=self.args.file,
            sep=self.args.separator,
            encoding=self.args.encoding,
            flatten=self.args.flatten,
            ignore_invalid=self.args.ignore,
        )
        counts = None
        sums = None
        for values in sp:
            if sums is None:
                sums = [0] * len(values)
                counts = [0] * len(values)

            for i in range(len(values)):
                val = values[i]
                if math.isnan(val):
                    continue
                sums[i] += values[i]
                counts[i] += 1

        safediv = lambda a, b: float("nan") if b == 0 else a / b

        means = [safediv(s, c) for s, c in zip(sums, counts)]
        print(" ".join(map(str, means)))
        return 0
