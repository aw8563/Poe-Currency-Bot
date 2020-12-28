#!/usr/bin/python3
from Bots.Utils.gameUtils import focusGame

class Bot:
    def __init__(self, steps):
        self.steps = steps

    def run(self):
        focusGame()

        # Initial character position should be at vendor
        while True:
            for step in self.steps:
                if not step():
                    return
