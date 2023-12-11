from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import os
import shutil


class GraphBuilder:

    def __init__(self,
                 output_image_path,
                 title = "",
                 ylabel = "",
                 labels = [],
                 time_label_format = "%Y-%m-%d %H:%M:%S",
                 time_span = timedelta(hours=1)):
        self.output_image_path = output_image_path
        self.time_label_format = time_label_format
        self.time_span = time_span

        root, ext = os.path.splitext(output_image_path)
        self.temp_image_path = root + ".tmp" + ext

        self.times = []
        self.values = []

        self.fig, self.ax = plt.subplots(figsize=(4, 6), layout="constrained")
        plt.title(title)
        plt.xlabel('Time')
        plt.ylabel(ylabel)

        # Create and store empty curves with labels, their data will be updated in 'add' method
        self.curves = []
        for l in labels:
            curve, = self.ax.plot([], [], label=l)
            self.curves.append(curve)
        plt.legend()

    def add(self, time, values):
        assert len(values)==len(self.curves)

        self.times.append(time)
        self.values.append(values)

        # Remove old values apart the "most recent old", it will be drawn outside the time axis
        # and ensure the line stays continuous
        max_time = time
        min_time = time - self.time_span
        for i, t in enumerate(self.times):
            if t<min_time and self.times[i+1]<min_time:
                self.times.pop(i)
                self.values.pop(i)
            else:
                break

        # Set x axis scale
        mid_time = min_time + (max_time - min_time) / 2
        xticks = [min_time, mid_time, max_time]
        xlabels = [x.strftime(self.time_label_format) for x in xticks]
        self.ax.set_xticks(xticks, labels=xlabels)
        self.ax.set_xlim(min_time, max_time)

        # Update curves
        for i, curve in enumerate(self.curves):
            curve.set_data(self.times, [v[i] for v in self.values])

        # Recompute y autoscale and draw
        self.ax.relim()
        self.ax.autoscale_view(scaley=True, scalex=False)
        self.fig.canvas.draw()

        # Write in a temp file and quick copy to output to avoid temporary broken file
        self.fig.savefig(self.temp_image_path)
        shutil.copy(self.temp_image_path, self.output_image_path)
