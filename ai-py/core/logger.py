from core.timer import Timer

__author__ = "Stefan Zaruba"


class Logging:
    """Used to log data streams to a CSV file"""

    file = None
    timer = Timer()

    # A list of Loggers
    loggers = []

    def __init__(self, file_path="../log/logfile.txt", flush_rate=10):
        """
        Initializes the Logging class

        :param file_path: file path of csv file to log to
        :param flush_rate: rate in ticks after which the logger should write to the csv file
        """

        self.file_path = file_path
        self.flush_rate = flush_rate

    class Logger:
        """Holds an observable of logged values."""

        name = ""  # descriptive label for logged values
        last_val = ""  # last logged value
        observable = None  # stream of logged values

        def __init__(self, name, obs):
            self.name = name
            self.observable = obs
            obs.subscribe(lambda x: setattr(self, "last_val", x))

    def on_tick(self, tick):
        self.write_line(tick)
        if tick % self.flush_rate == 0:
            self.file.flush()

    def start_logging(self):
        """Start logging to console and file"""

        self.file = open(self.file_path, "w")
        self.write_header()
        self.timer.ticks.subscribe(lambda x: self.on_tick(x))

    def add_logger(self, logger):
        """Add a logger. Imagine it as another column in the CSV file."""

        self.loggers.append(logger)

    def write_header(self):
        """Write the header of the CSV file, based on the Loggers' names"""

        header = "tick"
        header += ';'.join(map(lambda x: x.name, self.loggers))
        self.file.write(header + "\n")
        print(header)

    def write_line(self, tick):
        """Write a single line to the log CSV file."""

        line = f"{tick};"
        line += ';'.join(map(lambda x: str(x.last_val), self.loggers))

        # reset last value
        for logger in self.loggers:
            logger.last_val = ""

        self.file.write(line + "\n")
        print(line)
