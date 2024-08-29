from datetime import datetime, timedelta


class Timer:
    """
    Class to handle timing operations.
    """

    def __init__(self):
        self.start_time = None
        self.total_time = timedelta()


    def start(self):
        if self.start_time:
            self.start_time = datetime.now() - self.start_time
        elif self.start_time is None:
            self.start_time = datetime.now()


    def stop(self):
        if self.start_time:
            end_time = datetime.now()
            self.total_time = end_time - self.start_time
            self.start_time = None
            return end_time, self.total_time
        return None, None


    def reset(self):
        self.start_time = None
        self.total_time = timedelta()


    def get_elapsed_time(self):
        if self.start_time:
            return datetime.now() - self.start_time + self.total_time
        return self.total_time
