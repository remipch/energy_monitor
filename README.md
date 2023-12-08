# Energy Monitor

## Goal

Measure and display home electric energy production and consumption.

## Architecture

```
                               Raspberry Pi 3 B              Arduino Nano
                           ┌──────────────────────┐     ┌─────────────────────┐
                           │                      │     │                     │
                           │ ┌──────────────────┐ │ USB │ ┌─────────────────┐ │
                           │ │ graph_builder.py ├─┼─────┼─► rms_measure.ino │ │
                           │ └───────┬──────────┘ │     │ └─────────────────┘ │
                           │         │write       │     │                     │
                           │ ┌───────▼──────────┐ │     │                     │
          Client           │ │    graph.png     │ │     │                  a0 │-O
    ┌───────────────┐      │ └───────▲──────────┘ │     │                  a1 │--O
    │               │      │         │read        │     │                  a2 │---O
    │ ┌───────────┐ │ Wifi │ ┌───────┴──────────┐ │     │          analog  a3 │----O   current
    │ │web_browser├─┼──────┼─►  http_server.py  │ │     │          inputs  a4 │-----O   transformers
    │ └───────────┘ │      │ └───────┬──────────┘ │     │                  a5 │------O
    │               │      │         │read        │     │                  a6 │-------O
    └───────────────┘      │ ┌───────▼──────────┐ │     │                  a7 │--------O
                           │ │    index.html    │ │     │                     │
                           │ └──────────────────┘ │     │                     │
                           │                      │     │                     │
                           └──────────────────────┘     └─────────────────────┘
```

## Main steps

- Read Arduino analog inputs
- Compute RMS voltages in Arduino
- Read RMS voltages from Raspberry via USB serial port
- Convert from RMS voltages to milliamps, taking into account :
    - current transformer ratio
    - burden resistor
    - optional calibration
- Build a beautiful graph (python or fortran ?)
- Serve a simple web page over Wifi (minimal python web server)

## Serial protocol

Arduino listen commands from Raspberry and print measures as numerical text values.

Commands and measures are terminated by a new line character.

Arduino also print some comments (line starting with `#`).

### Custom separator

The default separator is a simple space, it can be changed with this command.

- Command: `s<separator>`
- Command example: `s;`

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
