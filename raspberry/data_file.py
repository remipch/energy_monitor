
# pip install pyserial

import csv
from datetime import datetime
import os

class DataFile:
    # File format (csv) :
    # - first line is the header
    # - next lines are data

    def __init__(self, path_prefix, header):
        self.path_prefix = path_prefix
        self.header = header
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

        path = self.path_prefix + now.strftime("%Y-%m-%d") + ".csv"
        if not os.path.isfile(path):
            print("No existing file: create new file")
            self.__createFile(path)

        elif self.file is None:
            print("Open existing file")
            self.__openFile(path)

        elif now.date() != self.previous_date:
            print("New day: close current file")
            self.close()
            self.__openFile(path)

        # Write and flush
        self.writer.writerow(values)
        self.file.flush()
        self.previous_date = now.date()

    def __createFile(self, path):
        self.__openFile(path)
        print("Write header")
        self.writer.writerow(self.header)

    def __openFile(self, path):
        print("Open file: ", path)
        self.file = open(path, 'a', newline='')
        self.writer = csv.writer(self.file)
