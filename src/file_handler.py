import csv

class CSVHandler:
    """
    Class to handle reading and writing to a CSV file.
    """

    def __init__(self, project_manager):
        self.file_path = project_manager.csv_file_path


    def write_log_entry(
        self,
        project,
        start_time,
        end_time,
        total_time,
        description=""
    ):
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                start_time.date(),
                start_time.time(),
                end_time.time(),
                total_time,
                project,
                description
            ])


    def read_project_time(self, project):
        total_time = 0
        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[4] == project:
                        total_time += self._convert_time_to_seconds(row[3])
        
        except FileNotFoundError:
            pass

        return total_time


    @staticmethod
    def _convert_time_to_seconds(time_str):
        time_str = time_str.split(".")[0]
        hours, minutes, seconds = map(int, time_str.split(":"))
        return hours * 3600 + minutes * 60 + seconds