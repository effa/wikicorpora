#!/usr/bin/env python
# encoding: utf-8

import sys


class ProgressBar(object):

    """Class for progress visualization"""

    def __init__(self):
        self.update(0.0)

    def update(self, progress):
        """(Re)draw progressbar with current progress
        """
        # progressbar length
        LENGTH = 20
        # progress should be between 0 and 1
        progress = max(0.0, min(progress, 1.0))
        done = int(progress * LENGTH)
        sys.stdout.write('\r[{bar}] {percentage}%'.format(
            bar=('#' * done).ljust(LENGTH),
            percentage=int(progress * 100)))
        sys.stdout.flush()

    def finish(self):
        self.update(1)
        print
