# Energy Monitor

## Goal

Measure and display home electric energy production and consumption.

## Architecture

```
                                      Raspberry Pi 3 B               Arduino Nano
                                  ┌───────────────────────┐     ┌─────────────────────┐
                        port 8001 │ ┌───────────────────┐ │     │                     │
                      ┌───────────┼─►    http server    │ │     │                     │
                      │           │ └────────┬──────────┘ │     │                     │
                      │           │          │ read       │     │                     │
                      │           │ ┌────────▼──────────┐ │     │                     │
                      │           │ │data/seconds/*.csv │ │     │                     │
         Client       │           │ │data/minutes/*.csv │ │     │                     │
   ┌───────────────┐  │           │ └────────▲──────────┘ │     │                     │
   │               │  │           │          │ write      │     │                     │
   │ ┌───────────┐ │  │           │ ┌────────┴──────────┐ │ USB │ ┌─────────────────┐ │
   │ │web_browser├─┼──┤           │ │data_recorder.py   ├─┼─────┼─► rms_measure.ino │ │
   │ └───────────┘ │  │           │ └────────┬──────────┘ │     │ └──────────┬──────┘ │
   │               │  │           │          │ write      │     │            │        │
   └───────────────┘  │           │ ┌────────▼──────────┐ │     │            │        │
                      │           │ │graphs/hour.svg    │ │     │       read │        │
                      │           │ │graphs/minute.svg  │ │     │            │        │
                      │           │ └────────▲──────────┘ │     │            │        │
                      │           │          │ read       │     │            │     a0 │
                      │ port 8000 │ ┌────────┴──────────┐ │     │            │     a1 │
                      └───────────┼─►    http server    │ │     │            ▼     a2 │
                                  │ └────────┬──────────┘ │     │          analog  a3 │
                                  │          │ read       │     │          inputs  a4 │
                                  │ ┌────────▼──────────┐ │     │                  a5 │
                                  │ │index.html         │ │     │                  a6 │
                                  │ │graph_view.html    │ │     │                  a7 │
                                  │ │style.css          │ │     │                     │
                                  │ └───────────────────┘ │     │                     │
                                  └───────────────────────┘     └─────────────────────┘
```

## Main steps

- Read Arduino analog inputs
- Compute RMS voltages in Arduino
- Read RMS voltages from Raspberry via USB serial port
- Convert from RMS voltages to milliamps, taking into account :
    - current transformer ratio
    - burden resistor
    - optional calibration
- Build graphs (last minute, last hour)
- Log measure data in timestamped files:
    - one file per day, one measure per second
    - one file per day, one measure per minute
- Publish results over Wifi (using python http server):
    - show graphs in minimal web page
    - allow to download measure data

## Folder structure

Source and generated files are in the following hardcoded folder structure :

```
Folder                  Description
----------------------  ---------------------
arduino/                Runs on Arduino
    rms_measure/        Measure analog inputs and compute RMS
raspberry/              Runs on Raspberry
    python/             Tools to record data and build graphs
    web/                Files required to serve http servers
        data/           Generated CSV files of recorded measures
            seconds/    One line per second
            minutes/    One line per minute
        graphs/         Generated SVG images
```

## Install

### Dependencies

```
pip install numpy==1.22.4
pip install pandas
pip install matplotlib==3.6
pip install ftfy
sudo apt-get install libatlas-base-dev
```

### Autostart

If Raspberry Pi has been installed with the default desktop,
autostart can be setup by adding the following lines
to `/etc/xdg/lxsession/LXDE-pi/autostart` :

```
@lxterminal -t web_interface -e bash /home/pi/energy_monitor/raspberry/run_web_interface.sh
@lxterminal -t web_data -e bash /home/pi/energy_monitor/raspberry/run_web_data.sh
@lxterminal -t data_recorder -e bash /home/pi/energy_monitor/raspberry/run_data_recorder.sh
@lxterminal -t minute_graph_builder -e bash /home/pi/energy_monitor/raspberry/run_minute_graph_builder.sh
@lxterminal -t hour_graph_builder -e bash /home/pi/energy_monitor/raspberry/run_hour_graph_builder.sh
```

(from https://forums.raspberrypi.com/viewtopic.php?t=294014)

## Serial protocol

Arduino listen commands from Raspberry and print measures as numerical text values.

Commands and measures are terminated by a new line character.

Arduino also print some comments (line starting with `#`).

### Custom separator

The default separator is a simple space, it can be changed with this command.

- Command: `s<separator>`
- Command example: `s;`

### Bufferized voltages

Measure and store unfiltered analog voltages as fast as possible.
Print them all when the buffer is full (100 samples).

- Command: `b`
- Output example:
```
# Bufferized input ; duration(ms): 89 ; samples_count: 100
# A7(mV) A6(mV) A5(mV) A4(mV) A3(mV) A2(mV) A1(mV) A0(mV)
0 3137 2453 2106 0 1119 1779 2424
0 1432 1730 1783 0 386 806 904
0 263 806 1129 0 63 259 39
0 0 180 547 0 0 4 0
0 0 0 146 0 0 0 0
0 122 43 0 0 0 9 366
0 381 263 151 0 24 73 645
0 625 527 386 0 53 141 943
0 869 806 664 0 83 195 1197
0 1080 1065 948 0 102 234 1368
[90 remaining lines]
```

### Unfiltered voltages

Continuously measure and print unfiltered analog voltages.

- Command: `u`
- Output example:
```
# Unfiltered input
# time(ms) A7(mV) A6(mV) A5(mV) A4(mV) A3(mV) A2(mV) A1(mV) A0(mV)
12120 3347 2624 2502 1715 1285 977 2614 2878
12123 3010 2864 2502 2218 1969 1739 2614 2878
12127 2937 2922 2502 2605 2624 2556 2614 2878
12131 2913 2922 2502 2639 2712 2693 2614 2878
12135 2869 2854 2502 2390 2306 2204 2619 2883
12139 2829 2790 2502 2243 2062 1901 2619 2883
12143 2834 2800 2502 2409 2346 2282 2619 2878
12147 2873 2864 2502 2673 2781 2844 2614 2878
12151 2888 2888 2502 2668 2776 2839 2619 2883
```

### RMS voltages

Continuously measure, compute and print RMS voltages over the given measure duration.

- Command: `r<measure_duration_ms>`
- Command example: `r500`
- Minimal measure duration: 40 ms
- Maximal measure duration: 10000 ms
- Output example:
```
# RMS voltage, measure_duration: 500 ms
# start_time(ms) end_time(ms) A6(mV) A5(mV) A4(mV) A3(mV) A2(mV) A1(mV) A0(mV) samples_count
32367 32868 39 351 386 439 498 239 39 288
32871 33372 24 356 386 434 493 239 24 288
33374 33874 24 356 386 439 498 239 24 288
33878 34379 24 356 386 439 498 239 24 289
34382 34882 24 356 386 434 493 239 24 288
34885 35386 24 356 386 434 493 239 24 288
35388 35888 24 356 386 434 493 239 24 287
```

### Stop measure

Any unknown command will stop measure.

## Material
- [Current transformers](https://www.gotronic.fr/art-capteur-de-courant-30-a-sct013-030-18987.htm)
- [Arduino Nano compatible board](https://www.gotronic.fr/art-carte-maker-nano-37259.htm)
- [Raspberry Pi 3 model B](https://www.etechnophiles.com/raspberry-pi-3-gpio-pinout-pin-diagram-and-specs-in-detail-model-b)

## References

Inspired from [OpenEnergyMonitor](https://docs.openenergymonitor.org/electricity-monitoring/ct-sensors/how-to-build-an-arduino-energy-monitor-measuring-current-only.html).
