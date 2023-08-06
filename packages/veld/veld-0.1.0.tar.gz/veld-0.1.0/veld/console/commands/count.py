# -*- coding: utf-8 -*-

import math

from veld.stream_processor import StreamProcessor

from .base import BaseCommand


class CountCommand(BaseCommand):
    def __init__(self):
        super().__init__(
            name="count",
            title="Count the number of values in the data stream",
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
        for values in sp:
            if counts is None:
                counts = [0] * len(values)

            for i in range(len(values)):
                val = values[i]
                if math.isnan(val):
                    continue
                counts[i] += 1

        print(" ".join(map(str, counts)))
        return 0
