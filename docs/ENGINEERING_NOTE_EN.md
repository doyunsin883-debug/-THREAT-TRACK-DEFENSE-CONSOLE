# THREAT-TRACK — Engineering Design Notes

> **Built and documented by Doyun Shin · Industrial Engineering, Gachon University**  
> [Project README](../README.md) · [한국어 설명](ENGINEERING_NOTE_KO.md) · [Validation plan](VALIDATION_PLAN.md)

## Why I built it

I began by connecting an HC-SR04 to an Arduino and checking the distance readings. Once that worked, I wanted to do more with the numbers. Knowing that an object is close is useful, but knowing how quickly it's approaching can be even more helpful. So I added speed and TTC estimates, then connected the results to LEDs, a buzzer, and a desktop dashboard.

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

I used different colors and beep patterns so the alert level would be recognizable without constantly reading the numbers. These are **prototype thresholds**; I haven't tested which thresholds would work best under real operating conditions.

[Alert-state diagram](../assets/charts/alert-decision-map.png) · [TTC model](../assets/charts/ttc-model.png)

## Desktop interface and serial integration

The firmware sends CSV records in the format `distance,speed,ttc,status`. The Python application reads these with `pyserial`, validates packets, and displays live measurements and status-change logs with `Tkinter`. The graphical scanning sweep is an **aesthetic presentation of single-axis range data**; it does not measure bearing or perform actual 360-degree radar scanning.

[Arduino source](../arduino/ThreatTrack_V5/ThreatTrack_V5.ino) · [Python source](../python/threat_track_dashboard.py) · [Executed demo-mode GUI screenshot](../assets/screenshots/dashboard-demo-screenshot.png)

The Python interface opens and the screenshot shows it running in demo mode. The values in that screenshot are simulated. I still need to confirm that V5 live readings update correctly after the COM5 port issue.

## Evidence and next validation

- **Observed during my build:** HC-SR04 output on Arduino Serial Monitor, three-color LED switching, audible buzzer operation, and Python GUI startup.
- **Not yet established:** absolute distance measurement error, approach-speed error, false-alarm rate, alert reaction latency, and continuous PC serial integration after the COM port issue.
- **Next steps:** repeat readings against fixed reference distances, log synchronized time series with controlled target motion, quantify uncertainty, and evaluate response lag. See [validation protocol](VALIDATION_PLAN.md).

This is an educational embedded-systems/HMI prototype, **not a military radar or safety-certified collision detector**.

[Media provenance](../assets/ASSET_PROVENANCE.md) · [Back to README](../README.md)
