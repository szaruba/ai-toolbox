from core.timer import Timer


class Logging:
    file = None
    timer = Timer()

    # A list of Loggers
    loggers = []

    def __init__(self, file_path="../log/logfile.txt", flush_rate=10):
        self.file_path = file_path
        self.flush_rate = flush_rate

    class Logger:
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
        self.loggers.append(logger)

    def write_header(self):
        header = "tick"
        header += ';'.join(map(lambda x: x.name, self.loggers))
        self.file.write(header + "\n")
        print(header)

    def write_line(self, tick):
        line = f"{tick};"
        line += ';'.join(map(lambda x: str(x.last_val), self.loggers))

        # reset last value
        for logger in self.loggers:
            logger.last_val = ""

        self.file.write(line + "\n")
        print(line)
