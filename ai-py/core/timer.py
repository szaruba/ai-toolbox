import rx
from rx.subject import Subject

__author__ = "Stefan Zaruba"


class Timer:
    """Singleton timer used for global time tracking"""

    class __Timer:
        ticks_per_second = 50
        ticks = rx.subject.Subject()  # Subscribe to this subject to receive the globally synchronized tick updates
        timer = rx.timer(0, 1.0/ticks_per_second)

    instance = None

    def __init__(self):
        if not Timer.instance:
            Timer.instance = Timer.__Timer()

    def start(self):
        """Starts the ticking"""

        self.instance.timer.subscribe(lambda x: self.instance.ticks.on_next(x))

    def __getattr__(self, item):
        return getattr(Timer.instance, item)