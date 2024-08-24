from datetime import datetime, timedelta


class Timer:
    """
    Class to handle timing operations.
    """

    def __init__(self):
        self.start_time = None
        self.paused_time = None
        self.total_time = timedelta()


    def start(self):
        if self.paused_time and self.start_time:
            self.start_time = datetime.now() - (self.paused_time - self.start_time)
            self.paused_time = None
        elif self.start_time is None:
            self.start_time = datetime.now()


    def pause(self):
        if self.start_time:
            self.paused_time = datetime.now()
            self.total_time += self.paused_time - self.start_time
            self.start_time = None


    def stop(self):
        if self.start_time:
            end_time = datetime.now()
            self.total_time += end_time - self.start_time
            self.start_time = None
            return end_time, self.total_time
        return None, None


    def reset(self):
        self.start_time = None
        self.paused_time = None
        self.total_time = timedelta()


    def get_elapsed_time(self):
        if self.start_time:
            return datetime.now() - self.start_time + self.total_time
        return self.total_time