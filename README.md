# Energy Monitor

## Goal

Measure and display home electric energy production and consumption.

## Architecture

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
- Example: `s;`

### Unfiltered voltages

Continuously measure and print unfiltered analog voltages.

- Command: `u`
- Output format : `time(ms) A7(V) A6(V) A5(V) A4(V) A3(V) A2(V) A1(V) A0(V)`

### RMS voltages

Continuously measure, compute and print RMS voltages over the given measure duration.

- Command: `r<measure_duration_ms>`
- Example: `r500`
- Minimal measure duration: 40 ms
- Maximal measure duration: 10000 ms
- Output format : `start_time(ms) end_time(ms) A6(Vrms) A5(Vrms) A4(Vrms) A3(Vrms) A2(Vrms) A1(Vrms) A0(Vrms) samples_count`

### Stop measure

Any unknown command will stop measure.

## Material
- [Current transformers](https://www.gotronic.fr/art-capteur-de-courant-30-a-sct013-030-18987.htm)
- [Arduino Nano compatible board](https://www.gotronic.fr/art-carte-maker-nano-37259.htm)
- [Raspberry Pi 3 model B](https://www.etechnophiles.com/raspberry-pi-3-gpio-pinout-pin-diagram-and-specs-in-detail-model-b)

## References

Inspired from [OpenEnergyMonitor](https://docs.openenergymonitor.org/electricity-monitoring/ct-sensors/how-to-build-an-arduino-energy-monitor-measuring-current-only.html).
