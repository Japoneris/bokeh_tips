# Sensor Monitor with Bokeh

Real-time visualization of Linux hardware sensors (CPU temperatures and fan speeds) using a live-updating Bokeh dashboard.

## Motivation

Existing Linux sensor tools either:
- Mix metrics with different units in a single unreadable plot
- Offer no easy way to record data over time

This project addresses both by displaying sensors in separate charts and streaming data via Bokeh.

## Features

- **Fan speed chart** — plots all fans in RPM over time
- **Temperature chart** — plots all CPU/chipset/WiFi temperature sensors in °C over time
- Separate graphs per unit for readability
- Live streaming at 500 ms intervals
- Interactive tools: pan, zoom, box/lasso select, hover tooltips, save

## Usage

```bash
bokeh serve --show fans.py
```

This opens a browser tab with the live dashboard. Data streams automatically as long as the server runs.

## Dependencies

- `psutil` — reads hardware sensor data from the OS
- `bokeh` — serves the interactive live-updating plots

## Files

| File | Description |
|------|-------------|
| `fans.py` | Main dashboard script |
| `test.py` | Prototype: basic Bokeh streaming with random data |
| `test_2.py` | Prototype: Bokeh streaming + slider (sine wave) |
| `01_test.ipynb` | Exploration notebook for `psutil` sensor APIs |
