# -*- coding: utf-8 -*-

import math

from collections import Counter

from veld.stream_processor import StreamProcessor

from .base import BaseCommand


class ModeCommand(BaseCommand):
    def __init__(self):
        super().__init__(
            name="mode",
            title="Find the mode of the values in the data stream",
        )

    def handle(self) -> int:
        sp = StreamProcessor(
            path=self.args.file,
            sep=self.args.separator,
            encoding=self.args.encoding,
            flatten=self.args.flatten,
            ignore_invalid=self.args.ignore,
        )

        counters = None
        for values in sp:
            if counters is None:
                counters = [Counter() for _ in range(len(values))]

            for i in range(len(values)):
                val = values[i]
                if math.isnan(val):
                    continue

                counters[i].update([val])

        mc = [c.most_common(1)[0] for c in counters]
        print(" ".join(map(str, mc)))
        return 0
