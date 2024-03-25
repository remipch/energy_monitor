from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
import os
import shutil
from collections import deque
from io import StringIO
import pandas as pd

# Input csv must :
# - respect name pattern: yyyy-mm-dd.csv
# - only contain values for a single day
# - have column 'hour' and 'minute'
# - eventually have column 'second'

# Minimal value for the max value of the y axis
MIN_CURRENT_MAX_SCALE = 15000 # (mA)
CURRENT_SCALE_MARGIN = 500 # (mA)

def __readDayCsvLastLines(input_csv_path, line_count):
    with open(input_csv_path , 'r') as f:
        q = [f.readline()] # read the header
        q.extend(deque(f, line_count))
        df = pd.read_csv(StringIO('\n'.join(q)))
        return df

def build_graph(input_directory,
                line_count, # last lines of input_csv_path to read
                columns,    # must match csv header
                labels,
                output_image_path,
                title = "",
                ylabel = "",
                time_label_format = "%Y-%m-%d %H:%M:%S",
                time_span = timedelta(hours=1)):

    assert len(columns)==len(labels)

    root, ext = os.path.splitext(output_image_path)
    temp_image_path = root + ".tmp" + ext

    now = datetime.now()
    input_csv_path = input_directory / (now.strftime("%Y-%m-%d") + ".csv")
    if not os.path.isfile(input_csv_path):
        return

    print("Update graph from ", input_csv_path)

    # Read last csv lines and add a time column
    # it's safe to convert to datetime because we have one file per day
    df = __readDayCsvLastLines(input_csv_path, line_count)
    if 'second' in df.columns:
        df['time'] = df['hour'].astype(str) + ':' + df['minute'].astype(str) + ':' + df['second'].astype(str)
        df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')
    else:
        df['time'] = df['hour'].astype(str) + ':' + df['minute'].astype(str)
        df['time'] = pd.to_datetime(df['time'], format='%H:%M')

    max_time = df['time'].max()
    min_time = max_time - time_span

    # Filter rows after min_time
    filtered_df = df[(df['time'] >= min_time)]
    print(f"  from {min_time.time()} to {max_time.time()} : {len(filtered_df)} measures")
    times = filtered_df['time']
    filtered_df = filtered_df[columns]

    # Create graph
    fig, ax = plt.subplots(figsize=(4, 6), layout="constrained")
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel(ylabel)

    # Set x axis scale
    mid_time = min_time + (max_time - min_time) / 2
    xticks = [min_time, mid_time, max_time]
    xlabels = [x.strftime(time_label_format) for x in xticks]
    ax.set_xticks(xticks, labels=xlabels)
    ax.set_xlim(min_time, max_time)

    # Set y axis scale
    max_current = MIN_CURRENT_MAX_SCALE
    for column in columns:
        max_current = max(max_current, filtered_df[column].max())
    ax.set_ylim(0, max_current + CURRENT_SCALE_MARGIN)

    # Draw curves
    for column, label in zip(columns, labels):
        ax.step(times, filtered_df[column], label=label)
    plt.legend()

    # Write in a temp file and quick copy to output to avoid temporary broken file
    os.remove(temp_image_path)
    plt.savefig(temp_image_path)
    os.remove(output_image_path)
    shutil.copy(temp_image_path, output_image_path)

