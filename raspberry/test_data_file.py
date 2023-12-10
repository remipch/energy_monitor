import os
from data_file import DataFile
from datetime import datetime
import tempfile

PATH_PREFIX = tempfile.gettempdir()+"/test_data_file-"
FIRST_PATH = PATH_PREFIX+"2023-12-10.csv"
SECOND_PATH = PATH_PREFIX+"2023-12-11.csv"

print("FIRST_PATH: ", FIRST_PATH)
print("SECOND_PATH: ", SECOND_PATH)

if os.path.isfile(FIRST_PATH):
    os.remove(FIRST_PATH)

if os.path.isfile(SECOND_PATH):
    os.remove(SECOND_PATH)

def assertFileContent(path, expected_content):
    assert os.path.isfile(path)
    with open(path, 'r') as file:
        content = file.read()
        assert content==expected_content,  "expected_content:\n" + expected_content + "content:\n" + content

data_file = DataFile(PATH_PREFIX, ["a","b"])

now = datetime(2023,12,10,15,47,12)
data_file.write(now, [1,10])
assertFileContent(FIRST_PATH, "a,b\n1,10\n")

now = datetime(2023,12,10,15,47,13)
data_file.write(now, [2,20])
assertFileContent(FIRST_PATH, "a,b\n1,10\n2,20\n")

# change day
now = datetime(2023,12,11,15,47,13)
data_file.write(now, [3,30])
assertFileContent(FIRST_PATH, "a,b\n1,10\n2,20\n")
assertFileContent(SECOND_PATH, "a,b\n3,30\n")
