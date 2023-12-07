# Energy Monitor

## Goal

Measure and display home electric energy production and consumption.

## Architecture

                                Raspberry Pi 3 B             Arduino Nano
                             ┌────────────────────┐     ┌─────────────────────┐
                             │                    │     │                     │
                             │ ┌────────────────┐ │ USB │ ┌─────────────────┐ │
                             │ │graph_builder.py├─┼─────┼─► rms_measure.ino │ │
                             │ └────────┬───────┘ │     │ └─────────────────┘ │
                             │          │         │     │                     │
                             │          ▼         │     │                     │
          Client             │      graph.png     │     │                  a0 │-O
    ┌─────────────────┐      │          ▲         │     │                  a1 │--O
    │                 │      │          │         │     │                  a2 │---O   current
    │  ┌───────────┐  │ Wifi │ ┌────────┴───────┐ │     │                  a3 │----O
    │  │web_browser├──┼──────┼─► http_server.py │ │     │                  a4 │-----O   transformers
    │  └───────────┘  │      │ └────────┬───────┘ │     │                  a5 │------O
    │                 │      │          │         │     │                  a6 │-------O
    └─────────────────┘      │          ▼         │     │                  a7 │--------O
                             │     index.html     │     │                     │
                             │                    │     │                     │
                             └────────────────────┘     └─────────────────────┘

## Main steps

- read currents with Arduino analog inputs
- compute RMS values in Arduino
- read RMS values from Raspberry via USB serial port
- convert from raw values to milliamps, taking into account :
    - current transformer ratio
    - burden resistor
    - optional calibration
- build a beautiful graph (python or fortran ?)
- serve a simple web page over Wifi (minimal python web server)

## Material
- [Current transformers](https://www.gotronic.fr/art-capteur-de-courant-30-a-sct013-030-18987.htm)
- [Arduino Nano compatible board](https://www.gotronic.fr/art-carte-maker-nano-37259.htm)
- [Raspberry Pi 3 model B](https://www.etechnophiles.com/raspberry-pi-3-gpio-pinout-pin-diagram-and-specs-in-detail-model-b)

## References

Inspired from [OpenEnergyMonitor](https://docs.openenergymonitor.org/electricity-monitoring/ct-sensors/how-to-build-an-arduino-energy-monitor-measuring-current-only.html).
