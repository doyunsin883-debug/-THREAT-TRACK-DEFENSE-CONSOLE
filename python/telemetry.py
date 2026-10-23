"""Telemetry packet parsing and classification for THREAT-TRACK."""
from dataclasses import dataclass
import math

STATES = {"SAFE", "WARNING", "DANGER"}

@dataclass(frozen=True)
class Telemetry:
    distance_cm: float
    approach_cm_s: float
    ttc_s: float | None
    status: str


def parse_packet(line: str) -> Telemetry | None:
    """Parse `<distance>,<speed>,<ttc>,<status>`.

    `NO_SIGNAL` means the sensor has no valid measurement, represented by None.
    Invalid/out-of-range packets raise ValueError rather than displaying bogus telemetry.
    """
    line = line.strip()
    if line == "NO_SIGNAL":
        return None
    items = line.split(",")
    if len(items) != 4:
        raise ValueError(f"Expected four CSV fields, got: {line[:160]}")
    d, speed, ttc = map(float, items[:3])
    status = items[3].strip()
    if any(not math.isfinite(v) for v in (d, speed, ttc)):
        raise ValueError("Non-finite telemetry")
    if not 2 <= d <= 400:
        raise ValueError("Out-of-range distance")
    if status not in STATES:
        raise ValueError("Unknown status")
    if ttc != -1 and ttc <= 0:
        raise ValueError("Invalid TTC sentinel")
    return Telemetry(d, speed, None if ttc == -1 else ttc, status)
