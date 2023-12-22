import csv
from datetime import datetime
from purge_data_directory import purge_data_directory
import os
from repair_csv import repair_last_csv_in_directory

class DataFile:
    # File format (csv) :
    # - first line is the header
    # - next lines are data
    # - end line is "\r\n"

    # max_size_bytes: auto remove data files when total data file size is greater
    def __init__(self, directory, header, max_size_bytes = None):
        self.directory = directory
        assert not os.path.isfile(self.directory)
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)
        self.header = header
        self.max_size_bytes = max_size_bytes

        # Try to repair the last csv file in the data folder
        # csv file can be corrupted if the system has been powered off
        # while DataFile was writing to it
        repair_last_csv_in_directory(directory, len(header))

    def write(self, now, values):
        assert len(values)==len(self.header)

        path = self.directory / (now.strftime("%Y-%m-%d") + ".csv")

        new_file = (not os.path.isfile(path)) or os.stat(path).st_size==0
        with open(path, 'a') as f:
            writer = csv.writer(f)
            if new_file:
                print("New file created: ", path)
                writer.writerow(self.header)
                if self.max_size_bytes is not None:
                    purge_data_directory(self.directory, self.max_size_bytes)

            writer.writerow(values)
