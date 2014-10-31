#!/usr/bin/env python
# encoding: utf-8

import sys


class ProgressBar(object):

    """Class for progress visualization"""

    def __init__(self, total=100):
        self._total = total
        self._done = 0
        self.update(0.0)

    def add(self, amount):
        """Adds :amount: to done work a redraw progressbar
        """
        self.update(self._done + amount)

    def finish(self):
        self.update(self._total)
        print

    def draw(self):
        """Print progress bar representing current progress
        """
        # progressbar length
        LENGTH = 20
        pieces_done = int(self.get_progress() * LENGTH)
        # print progress bar
        sys.stdout.write('\r[{bar}] {percentage:.2f} %'.format(
            bar=('#' * pieces_done).ljust(LENGTH),
            percentage=100.0 * self.get_progress()))
        sys.stdout.flush()

    def get_progress(self):
        """Calculate current progress

            Returns: float (between 0 and 1)
        """
        return float(self._done) / self._total

    def update(self, done):
        """Sets how many pieces of work are done and (re)draw progressbar
        """
        # self._done has to be in interval [0; self._total]
        self._done = max(0, min(done, self._total))
        self.draw()
