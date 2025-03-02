#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from pyclipcounter.appui import PyClipCounterUI


class PyClipCounter(PyClipCounterUI):
    def __init__(self, master=None):
        super().__init__(master)


if __name__ == "__main__":
    app = PyClipCounter()
    app.run()
