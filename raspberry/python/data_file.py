import csv
from datetime import datetime
from purge_data_directory import purge_data_directory
import os

class DataFile:
    # File format (csv) :
    # - first line is the header
    # - next lines are data

    # max_size_bytes: auto remove data files when total data file size is greater
    def __init__(self, directory, header, max_size_bytes = None):
        self.directory = directory
        assert not os.path.isfile(self.directory)
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)
        self.header = header
        self.max_size_bytes = max_size_bytes
        self.file = None
        self.writer = None
        self.previous_date = None

    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None
        self.writer = None
        self.previous_date = None

    def write(self, now, values):
        assert len(values)==len(self.header)

        path = self.directory / (now.strftime("%Y-%m-%d") + ".csv")

        if self.file is None:
            self.__openFile(path)

        elif now.date() != self.previous_date:
            print("New day: close current file and open new file")
            self.close()
            self.__openFile(path)

        # Write and flush
        self.writer.writerow(values)
        self.file.flush()
        self.previous_date = now.date()

    def __openFile(self, path):
        if os.path.isfile(path):
            print("Open existing file: ", path)
            self.file = open(path, 'a', newline='')
            self.writer = csv.writer(self.file)
        else:
            print("Create new file: ", path)
            if self.max_size_bytes is not None:
                purge_data_directory(self.directory, self.max_size_bytes)
            self.file = open(path, 'a', newline='')
            self.writer = csv.writer(self.file)
            self.writer.writerow(self.header)

