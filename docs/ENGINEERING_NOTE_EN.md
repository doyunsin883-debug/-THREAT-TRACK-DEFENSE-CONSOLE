# THREAT-TRACK — Engineering Design Notes

> **Built and documented by Doyun Shin · Industrial Engineering, Gachon University**  
> [Project README](../README.md) · [한국어 설명](ENGINEERING_NOTE_KO.md) · [Validation plan](VALIDATION_PLAN.md)

## Why I built it

My initial hardware experiment simply measured the distance between an HC-SR04 ultrasonic sensor and an object. I wanted to turn that one-dimensional reading into actionable information: **whether a target was approaching, how quickly it was approaching, how urgent the situation was, and what feedback an operator should receive**. I implemented the resulting sensing → estimation → rule-based classification → LED/buzzer actuation → desktop monitoring pipeline in stages.

## Hardware and pin assignment

| Component | Pin | Purpose |
|---|---|---|
| Arduino UNO | USB | Central control and serial transfer |
| HC-SR04 | TRIG D2, ECHO D3, 5V, GND | Forward-range measurement |
| Red LED | D4 with series resistor | DANGER |
| Yellow LED | D5 with series resistor | WARNING |
| Green LED | D6 with series resistor | SAFE |
| Low-current piezo buzzer | D7, GND | Audible alerts |

I used a shared ground rail. Each LED requires a separate current-limiting resistor. In the documented breadboard example, the buzzer is placed with positive at `e27` and negative at `e30`; jumpers connect `a27` to D7 and `a30` to the grounded rail.

[Hardware photo](../assets/screenshots/hardware-prototype.jpg) · [Wiring CAD](../assets/diagrams/wiring-cad.png) · [Editable DXF](cad/threat-track-schematic.dxf)

## Signal processing and risk logic

```text
distance_cm = echo_duration_microseconds × 0.0343 / 2
smoothed_distance = 0.4 × new_distance + 0.6 × previous_smoothed_distance
approach_speed = (previous_distance − current_distance) / elapsed_seconds
smoothed_speed = 0.5 × instantaneous_speed + 0.5 × previous_smoothed_speed
time_to_contact = distance / approach_speed   (only if speed > 10 cm/s)
```

Positive speed means the object is approaching the transducer; negative speed means it is receding. Exponential smoothing reduces short-term fluctuations, though it also adds response lag. Time-to-contact is an **indicative constant-velocity model for a directly approaching object**, not a validated prediction of impact.

| State | Policy condition | Output |
|---|---|---|
| SAFE | Distance > 70 cm and no TTC warning | Green LED, silence |
| WARNING | Distance ≤ 70 cm or TTC ≤ 3.0 s, excluding DANGER | Yellow LED, slow beep |
| DANGER | Distance ≤ 30 cm or TTC ≤ 1.5 s | Red LED, fast beep |
| NO SIGNAL | Invalid echo measurement | LEDs off, silence |

The thresholds are programmable **prototype decision rules**, not measured false-alarm or safety-performance guarantees. The different LED colors and sound cadences are intended to reduce the need for continuous numeric monitoring.

[Alert-state diagram](../assets/charts/alert-decision-map.png) · [TTC model](../assets/charts/ttc-model.png)

## Desktop interface and serial integration

The firmware sends CSV records in the format `distance,speed,ttc,status`. The Python application reads these with `pyserial`, validates packets, and displays live measurements and status-change logs with `Tkinter`. The graphical scanning sweep is an **aesthetic presentation of single-axis range data**; it does not measure bearing or perform actual 360-degree radar scanning.

[Arduino source](../arduino/ThreatTrack_V5/ThreatTrack_V5.ino) · [Python source](../python/threat_track_dashboard.py) · [Executed demo-mode GUI screenshot](../assets/screenshots/dashboard-demo-screenshot.png)

The Python GUI was observed opening, but successful live V5 serial refresh **remains to be verified** after an observed COM5 access conflict. The screenshot uses clearly labeled simulated values, not live sensor measurements.

## Evidence and next validation

- **Observed during my build:** HC-SR04 output on Arduino Serial Monitor, three-color LED switching, audible buzzer operation, and Python GUI startup.
- **Not yet established:** absolute distance measurement error, approach-speed error, false-alarm rate, alert reaction latency, and continuous PC serial integration after the COM port issue.
- **Next steps:** repeat readings against fixed reference distances, log synchronized time series with controlled target motion, quantify uncertainty, and evaluate response lag. See [validation protocol](VALIDATION_PLAN.md).

This is an educational embedded-systems/HMI prototype, **not a military radar or safety-certified collision detector**.

[Media provenance](../assets/ASSET_PROVENANCE.md) · [Back to README](../README.md)
