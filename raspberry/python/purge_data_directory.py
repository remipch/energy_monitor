import os
import fnmatch

# data files pattern, such as : 2023-12-25.csv
PATTERN = '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].csv'

def purge_data_directory(directory, max_size_bytes):
    print("purge_data_directory:")
    print("  directory: ", directory)
    print("  max_size_bytes: ", max_size_bytes)

    # First: compute size
    total_size = 0
    data_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        # Filter the filenames based on the pattern
        matching_filenames = fnmatch.filter(filenames, PATTERN)
        for filename in matching_filenames:
            if not os.path.islink(filename):
                data_file = os.path.join(dirpath, filename)
                total_size += os.path.getsize(data_file)
                data_files.append(data_file)
    print("  total_size: ", total_size)

    # Then: purge eventually
    if total_size <= max_size_bytes:
        print("  nothing to purge")
        return

    # because of chosen pattern: sort by name = sort by date
    data_files.sort()
    for data_file in data_files:
        print("  remove: ", data_file)
        total_size = total_size - os.path.getsize(data_file)
        os.remove(data_file)
        print("  total_size: ", total_size)
        if total_size < max_size_bytes:
            return
