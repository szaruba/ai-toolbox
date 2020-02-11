from abc import ABC, abstractmethod


class Component(ABC):
    inputs = {}  # dictionary of input streams
    outputs = {}  # dictionary of output streams

    meta = {}  # dictionary of meta information

    def __init__(self):
        pass

    def input_info(self):
        """"Provides information about this component's input streams"""
        pass

    def output_info(self):
        """"Provides information about this component's output streams"""
        pass
