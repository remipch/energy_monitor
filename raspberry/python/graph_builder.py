from datetime import datetime, timedelta
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

class GraphBuilder:

    def __init__(self,
                 input_directory,
                 line_count, # last lines of input_csv_path to read
                 columns,    # must match csv header
                 labels,
                 output_image_path,
                 title = "",
                 ylabel = "",
                 time_label_format = "%Y-%m-%d %H:%M:%S",
                 time_span = timedelta(hours=1)):

        assert len(columns)==len(labels)

        self.input_directory = input_directory
        self.line_count = line_count
        self.columns = columns
        self.output_image_path = output_image_path
        self.time_label_format = time_label_format
        self.time_span = time_span

        root, ext = os.path.splitext(output_image_path)
        self.temp_image_path = root + ".tmp" + ext

        self.times = []
        self.values = []

        self.modification_time = None

        self.fig, self.ax = plt.subplots(figsize=(4, 6), layout="constrained")
        plt.title(title)
        plt.xlabel('Time')
        plt.ylabel(ylabel)

        # Create and store empty curves with labels, their data will be updated in 'update' method
        self.curves = []
        for l in labels:
            curve, = self.ax.plot([], [], label=l)
            self.curves.append(curve)
        plt.legend()


    def __readDayCsvLastLines(self, input_csv_path):
        with open(input_csv_path , 'r') as f:
            q = [f.readline()] # read the header
            q.extend(deque(f, self.line_count))
            df = pd.read_csv(StringIO('\n'.join(q)))
            return df

    # Recompute and save graph if file has been modified
    def update(self, now):
        input_csv_path = self.input_directory / (now.strftime("%Y-%m-%d") + ".csv")

        modification_time = os.path.getmtime(input_csv_path)

        if self.modification_time == modification_time:
            return

        print("Update graph from ", input_csv_path)
        self.modification_time = modification_time

        # Read last csv lines and add a time column
        # it's safe to convert to datetime because we have one file per day
        df = self.__readDayCsvLastLines(input_csv_path)
        if 'second' in df.columns:
            df['time'] = df['hour'].astype(str) + ':' + df['minute'].astype(str) + ':' + df['second'].astype(str)
            df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S') #.dt.time
        else:
            df['time'] = df['hour'].astype(str) + ':' + df['minute'].astype(str)
            df['time'] = pd.to_datetime(df['time'], format='%H:%M') #.dt.time

        max_time = df['time'].max()
        min_time = max_time - self.time_span

        # Filter rows after min_time
        filtered_df = df[(df['time'] >= min_time)]
        print(filtered_df)
        times = filtered_df['time']
        filtered_df = filtered_df[self.columns]

        # Set x axis scale
        mid_time = min_time + (max_time - min_time) / 2
        xticks = [min_time, mid_time, max_time]
        xlabels = [x.strftime(self.time_label_format) for x in xticks]
        self.ax.set_xticks(xticks, labels=xlabels)
        self.ax.set_xlim(min_time, max_time)

        # Update curves
        for column, curve in zip(self.columns, self.curves):
            curve.set_data(times, filtered_df[column])

        # Recompute y autoscale and draw
        self.ax.relim()
        self.ax.autoscale_view(scaley=True, scalex=False)
        self.fig.canvas.draw()

        # Write in a temp file and quick copy to output to avoid temporary broken file
        self.fig.savefig(self.temp_image_path)
        shutil.copy(self.temp_image_path, self.output_image_path)
