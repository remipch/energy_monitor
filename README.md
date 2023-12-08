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
# time(ms) A7(V) A6(V) A5(V) A4(V) A3(V) A2(V) A1(V) A0(V)
1226783 2.71 2.59 2.50 2.35 2.26 2.21 2.61 2.88
1226787 2.81 2.71 2.50 2.35 2.20 2.07 2.61 2.88
1226792 2.83 2.77 2.50 2.36 2.22 2.10 2.61 2.88
1226797 2.84 2.81 2.50 2.49 2.47 2.42 2.62 2.88
1226801 2.87 2.84 2.50 2.58 2.63 2.64 2.61 2.88
1226805 2.87 2.84 2.50 2.50 2.49 2.46 2.62 2.88
1226810 2.85 2.82 2.50 2.39 2.29 2.21 2.62 2.88
1226814 2.85 2.82 2.50 2.42 2.36 2.32 2.62 2.88
1226818 2.86 2.84 2.50 2.55 2.59 2.60 2.61 2.88
1226823 2.87 2.85 2.50 2.57 2.61 2.62 2.61 2.88
1226827 2.86 2.84 2.50 2.44 2.39 2.33 2.61 2.88
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
# start_time(ms) end_time(ms) A6(Vrms) A5(Vrms) A4(Vrms) A3(Vrms) A2(Vrms) A1(Vrms) A0(Vrms) samples_count
1143884 1144384 0.05 0.36 0.39 0.43 0.47 0.24 0.03 288
1144388 1144889 0.02 0.36 0.38 0.41 0.44 0.24 0.02 288
1144893 1145394 0.02 0.36 0.38 0.41 0.44 0.24 0.02 288
1145398 1145899 0.02 0.36 0.38 0.41 0.44 0.24 0.02 288
1145903 1146404 0.02 0.36 0.38 0.41 0.44 0.24 0.02 289
1146408 1146909 0.02 0.36 0.38 0.41 0.44 0.24 0.02 288
1146913 1147414 0.02 0.36 0.38 0.41 0.44 0.24 0.02 288
```

### Stop measure

Any unknown command will stop measure.

## Material
- [Current transformers](https://www.gotronic.fr/art-capteur-de-courant-30-a-sct013-030-18987.htm)
- [Arduino Nano compatible board](https://www.gotronic.fr/art-carte-maker-nano-37259.htm)
- [Raspberry Pi 3 model B](https://www.etechnophiles.com/raspberry-pi-3-gpio-pinout-pin-diagram-and-specs-in-detail-model-b)

## References

Inspired from [OpenEnergyMonitor](https://docs.openenergymonitor.org/electricity-monitoring/ct-sensors/how-to-build-an-arduino-energy-monitor-measuring-current-only.html).
