from abc import ABC

__author__ = "Stefan Zaruba"


class Component(ABC):
    """
    The central building block for building an agent.

    An agent is comprised of multiple of such interacting components. Each component can have multiple input and
    output streams, through which it communicates with other components. Input streams must be prefixed by 'input_' and
    output streams are prefixed by 'output_'. Output streams must be of type rx.Observable, while input streams must
    be of type rx.subject.Subject.

    Output streams are used to transmit information to other components, while input streams are used to receive
    information from other components. Finally, components will be connected by piping values produced by the output
    streams into the input streams of other components.
    """

    def __init__(self):
        pass
