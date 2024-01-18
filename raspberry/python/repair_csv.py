from ftfy import fix_and_explain
from glob import glob
import os
import shutil

def repair_last_csv_in_directory(directory_path, csv_fields_count):
    pattern = f"{directory_path}/????-??-??.csv"
    sorted_files = sorted(glob(pattern), key=os.path.basename)
    if len(sorted_files)==0:
      return
    last_csv_file = sorted_files[-1]
    repair_csv(last_csv_file, csv_fields_count)

# Try to repair the given csv file :
# - remove all lines containing bad encoding
# - remove all lines containing the wrong number of csv fields
def repair_csv(csv_path, csv_fields_count):
    print(f"Try to detect problems in {csv_path}")
    with open(csv_path, 'r') as f:
        csv_data = f.read()

    # Make a copy in case of problem with the fix
    shutil.copy(csv_path, os.path.dirname(csv_path) + "/latest.csv.bak")

    problem_count = 0
    with open(csv_path, 'w') as f:
        for line in csv_data.splitlines():
            fixed, explanation = fix_and_explain(line)
            if len(explanation)>0:
                print(f"  Corrupted, remove line: {line}")
                problem_count = problem_count + 1
            elif len(line.split(","))!=csv_fields_count:
                print(f"  Wrong number of fields, remove line: {line}")
                problem_count = problem_count + 1
            else:
                f.write(line + "\r\n")

    if problem_count==0:
        print("  No problem detected")
    else:
        print(f"  {problem_count} problems detected")
