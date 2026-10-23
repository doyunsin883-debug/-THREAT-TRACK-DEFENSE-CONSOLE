# THREAT-TRACK · Tactical Proximity Defense Console
### 초음파 기반 전술형 근접 위협 감지·관제 시스템

[![Arduino UNO](https://img.shields.io/badge/Hardware-Arduino%20UNO-00979D?logo=arduino&logoColor=white)](arduino/ThreatTrack_V5/ThreatTrack_V5.ino)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](python/threat_track_dashboard.py)
[![Documentation](https://img.shields.io/badge/Docs-EN%20%2B%20KO-2E8B57)](docs/)
[![Stage](https://img.shields.io/badge/Stage-Working%20Prototype-F3AD35)](#project-status--프로젝트-진행-상태)
[![Tests](https://img.shields.io/badge/Checks-4%20unit%20tests-blue)](tests/test_telemetry.py)

**EN** · A single-axis ultrasonic proximity monitor that estimates approach speed, derives indicative time-to-contact (TTC), and issues three-level LED and buzzer alerts, with a tactical-style Python visualization.  
**KO** · 초음파 센서로 정면 물체의 거리와 접근 속도를 추정하고, 예상 접촉 시간(TTC)에 따라 3단계 LED·부저 경보를 작동시키는 아두이노 기반 시스템입니다. PC에는 전술형 관제 화면을 표시합니다.

> **Scope / 범위** · This is an educational **ultrasonic proximity demonstrator, not a radio-frequency military radar**. A single HC-SR04 cannot identify bearing, track multiple targets, or provide safety-critical collision detection. / 교육·시연용 **초음파 근접 탐지기**이며 군용 전파 레이더가 아닙니다. 센서 1개로 방향·다중 표적·안전 인증된 충돌 감지는 할 수 없습니다.

## Project at a glance / 첫 화면: 실제 사진과 설계도

| **Real prototype photo / 실제 제작 사진** | **CAD wiring diagram / CAD 배선도** |
|:---:|:---:|
| ![Arduino and HC-SR04 assembled on breadboard](assets/screenshots/hardware-prototype.jpg) | ![Verified logical pin assignments, annotated wiring CAD](assets/diagrams/wiring-cad.png) |
| **Recorded hardware photo** — Arduino UNO, HC-SR04, breadboard / **실제 촬영 사진** — 아두이노와 센서 | **Technical schematic** — schematic-level connections, not a measured PCB layout / **기술 배선도** — 핀 배치 기반 설계도 |

| **Actual serial output / 실제 시리얼 출력** | **Tactical dashboard / 전술형 관제 화면** |
|:---:|:---:|
| ![Actual Arduino IDE serial monitor output](assets/screenshots/serial-monitor.jpg) | ![Python dashboard running with explicitly simulated telemetry](assets/screenshots/dashboard-demo-screenshot.png) |
| **Actual screenshot** — ultrasonic range measurements / **실제 캡처** — 거리 측정값 출력 | **Actual screenshot of the Python GUI in `--demo` mode (simulated values)** — *not* live telemetry / **실제로 실행한 Python GUI의 데모 모드 캡처** — 가상 데이터, 실측 아님 |

**Design files / 설계 파일:** [Editable AutoCAD-compatible DXF](docs/cad/threat-track-schematic.dxf) · [SVG wiring schematic](assets/diagrams/wiring-cad.svg) · [System flow](assets/diagrams/system-flow.svg)

## Engineering objective / 프로젝트의 핵심 목적

**EN — Problem:** A raw distance number is not an actionable warning. An approaching object at 75 cm may require attention sooner than an object stationary at 50 cm. The design question is how to turn **one low-cost, single-axis ultrasonic measurement** into interpretable proximity telemetry and escalating local/desktop alerts.

**KO — 문제 정의:** 거리 숫자 하나만으로는 위험 상황을 판단하기 어렵습니다. 75cm 거리에서 빠르게 접근하는 물체는 50cm 거리에서 정지해 있는 물체보다 먼저 주의할 필요가 있을 수 있습니다. 따라서 **저비용 단일축 초음파 센서**에서 얻는 정보를 해석 가능한 거리·접근 속도·TTC·경보 단계로 전환하는 것이 핵심 목적입니다.

| Engineering question / 기술적 질문 | Implementation / 구현 방식 | Validation status / 검증 상태 |
|---|---|---|
| Can we read physical range? / 실제 거리 측정 가능한가? | HC-SR04 + Arduino timing | ✅ Observed on user-recorded Serial Monitor / 실제 시리얼 사진 확인 |
| Can we infer approach? / 접근·이탈을 구분할 수 있는가? | Smoothed finite-difference speed / 거리 차분 및 평활 | ✅ Reported working by builder / 사용자 동작 확인 보고; 정밀 검증 전 |
| Can we make actionable alerts? / 경보로 바꿀 수 있는가? | Distance + TTC thresholds → 3 LEDs + buzzer | ✅ User-reported hardware operation / 사용자 성공 보고 |
| Can operators inspect the state? / PC에서 관제할 수 있는가? | Serial CSV + Tkinter GUI | ✅ GUI opens; live packet refresh pending / GUI 실행 확인, 실시간 갱신 재검증 필요 |

**What is not claimed / 주장하지 않는 사항:** Object tracking in 2D or 3D, 360° scanning, target identification, military-grade detection, calibration-grade accuracy, false-alarm performance, or a deployed safety product. / 다차원 표적 추적, 360도 탐지, 목표 식별, 군용 성능, 계측기급 정확도, 오경보 성능 및 실제 안전장치 성능은 주장하지 않습니다.

## Evidence and Matplotlib analysis / 실제 증거 및 Matplotlib 분석

The plots below are reproducible using [`analysis/generate_figures.py`](analysis/generate_figures.py). **One uses only the eight distance values legible in the user's original Serial Monitor photo; the remaining figures visualize the mathematical rules in the firmware and are not experimental results.** / 아래 그래프는 코드로 재현할 수 있습니다. **첫 그래프만 사용자가 촬영한 실제 시리얼 모니터 사진에서 확인한 8개 측정값이며, 나머지는 펌웨어 수학 규칙의 이론적 도식입니다.**

### A. Recorded range samples / 시리얼 화면의 실제 거리값

![Actual Arduino range values transcribed from photograph](assets/charts/serial-readings-photo.png)

**EN:** Eight visible HC-SR04 range readings, in display order; no timestamps or ground-truth reference distance were supplied. Therefore this is evidence of sensor output, **not an accuracy or speed benchmark**.

**KO:** 사진에서 읽을 수 있는 HC-SR04 거리 8개를 표시 순서대로 옮겼습니다. 타임스탬프나 실제 기준 거리 데이터가 없어 **정확도 검증·속도 추정 결과로 해석하지 않습니다.** Values are recorded in [`data/serial_monitor_photo_readings.csv`](data/serial_monitor_photo_readings.csv).

### B. Why distance and speed both matter / 거리와 속도를 함께 고려하는 이유

![Distance-speed alert classification defined by firmware](assets/charts/alert-decision-map.png)

**EN:** Deterministic alert states from the exact V5 distance and TTC thresholds. Each colored region is the **software's decision**, not an observed classification accuracy. At high approach speed, even an object outside the 70-cm caution band can enter WARNING or DANGER via TTC.

**KO:** V5 코드에 정의된 거리 및 TTC 경계로 색 영역을 계산했습니다. **색 영역은 소프트웨어의 판정 규칙이지 실험적으로 측정한 정확도가 아닙니다.** 접근 속도가 높으면 70cm 밖에서도 TTC 기준에 따라 경고가 먼저 발생할 수 있습니다.

### C. Interpreting TTC / 예상 접촉 시간의 물리적 의미

![Constant speed TTC equation visualization](assets/charts/ttc-model.png)

**EN:** `TTC = distance / approaching_speed` under a constant-speed, directly approaching object assumption. This model demonstrates how identical range can imply different urgency depending on relative speed.

**KO:** 일정한 속도로 센서 정면에 접근한다고 가정했을 때 `TTC = 거리 / 접근 속도`를 시각화합니다. 같은 거리라도 접근 속도가 다르면 위험 판단 시점이 달라짐을 설명합니다.

**Recreate all three figures / 그래프 전체 재생성:**

```powershell
py -m pip install -r analysis/requirements.txt
py analysis/generate_figures.py
```

## Actual firmware and UI capture / 실제 개발 화면 기록

| **Arduino IDE firmware excerpt / 실제 아두이노 IDE 코드 촬영본** | **Python graphical interface / 실행된 Python GUI** |
|:---:|:---:|
| ![Original Arduino IDE photo, code being prepared for PC CSV output](assets/screenshots/arduino-ide-code-photo.jpg) | ![Tkinter dashboard actual screenshot, demo mode](assets/screenshots/dashboard-demo-screenshot.png) |
| *User-taken photo of the V5 PC-telemetry output code during an upload attempt; that attempt showed a COM5 error.* / *V5 출력 코드 업로드 시도 중 촬영한 원본 사진. 당시에는 COM5 오류 발생.* | *Actually captured Python program running in clearly labeled simulation mode, not live sensor telemetry.* / *프로그램 실제 실행 캡처이며 데모 가상값으로 표시. 실측 화면 아님.* |

> **No AI-rendered images are used. / AI 생성 그림 미사용.** Photography is user-provided; figures were produced from Matplotlib; wiring diagrams are manually constructed vector/CAD schematics; GUI capture comes from an executed Tkinter program. / 사진은 사용자가 보낸 원본이며, 그래프는 Matplotlib, 배선도는 직접 제작한 벡터 CAD, UI 캡처는 Python 실행 화면을 사용했습니다.

## How it works / 작동 원리

![Signal processing and alert workflow](assets/diagrams/system-flow.png)

| Module / 기능 | English | 한국어 |
|---|---|---|
| Sensor | HC-SR04 provides echo pulse width, converted to round-trip range | 반사파 왕복 시간으로 거리 계산 |
| Filtering | Exponential smoothing (distance: α = 0.4; speed: α = 0.5) | 거리와 속도의 지수평활 처리 |
| Velocity | Positive value indicates approaching; negative means retreating | 양수: 접근, 음수: 멀어짐 |
| TTC | `distance / approach_speed` only when approach speed exceeds 10 cm/s | 접근 속도가 10 cm/s 초과일 때 TTC 추정 |
| Decision | SAFE / WARNING / DANGER from distance or TTC | 거리 또는 TTC 조건에 따른 3단계 판정 |
| Actuation | D4–D6 LEDs, D7 buzzer; serial output to PC | LED·부저 경고 및 USB 시리얼 출력 |

### Core equations / 핵심 공식

```text
Distance [cm]     = echo_pulse_width [microseconds] × 0.0343 / 2
Smoothed distance = 0.4 × raw_distance + 0.6 × previous_smoothed_distance
Approach speed    = (previous_distance − current_distance) / elapsed_seconds
Smoothed speed    = 0.5 × instant_speed + 0.5 × previous_smoothed_speed
TTC [s]           = distance / approach_speed  (only while approaching > 10 cm/s)
```

These are illustrative approximations; distance noise and measurement geometry can make velocity and TTC fluctuate. / 위 값은 근사치이며 초음파의 측정 잡음, 반사 각도 등에 의해 속도와 TTC가 크게 변할 수 있습니다.

### Alert matrix / 경보 기준표

| Status | Distance / TTC condition | LED | Buzzer | 한국어 |
|---|---|---|---|---|
| SAFE | `d > 70 cm` **and** no TTC warning | Green | Silent | 안전: 초록 / 무음 |
| WARNING | `d ≤ 70 cm` or `0 < TTC ≤ 3.0 s` (excluding DANGER) | Yellow | Slow pulses | 주의: 노랑 / 느린 경고음 |
| DANGER | `d ≤ 30 cm` or `0 < TTC ≤ 1.5 s` | Red | Fast pulses | 위험: 빨강 / 빠른 경고음 |
| NO_SIGNAL | Invalid ultrasonic measurement | LEDs off | Silent | 무효 신호: 표시·경보 꺼짐 |

## Wiring / 배선

![Detailed pin map](assets/diagrams/wiring-cad.png)

| Component / 부품 | Arduino UNO | Connection / 연결 |
|---|---|---|
| HC-SR04 | 5V, GND, D2, D3 | `VCC→5V`, `GND→GND`, `TRIG→D2`, `ECHO→D3` |
| Red LED / 빨간 LED | D4 | `D4→series resistor→LED (+)`, `LED (−)→GND` |
| Yellow LED / 노란 LED | D5 | `D5→series resistor→LED (+)`, `LED (−)→GND` |
| Green LED / 초록 LED | D6 | `D6→series resistor→LED (+)`, `LED (−)→GND` |
| 2-pin buzzer / 2핀 부저 | D7 | `D7→buzzer (+)`, `buzzer (−)→GND` |

![Buzzer breadboard wiring, holes e27 and e30](assets/diagrams/buzzer-breadboard.png)

**Breadboard detail / 브레드보드 실제 예시:** buzzer positive at `e27`, negative at `e30`. Connect `a27→D7` and `a30→GND rail`. On a standard breadboard, `a27~e27` are internally connected and separated from `a30~e30`. / 부저 `+ = e27`, `− = e30`; `a27`은 D7, `a30`은 GND 레일에 연결합니다. `a~e` 동일 번호 줄끼리만 연결됩니다.

**Safety / 안전:** Disconnect USB before rewiring. Each LED requires its **own series current-limiting resistor** (typically 220–1,000 Ω depending on brightness). Only drive a confirmed low-current piezo buzzer directly from D7; higher-current units need a transistor driver. / 배선 변경 전 USB를 분리하고, LED마다 전류 제한 저항을 하나씩 사용하세요. 고전류 부저는 D7에 직접 연결하지 마세요.

> The CAD file is a **logical electrical schematic**, not a dimensionally verified reproduction of each jumper wire. The LCD and potentiometer seen in the parts inventory are not implemented in V5. / 본 CAD는 **전기적 연결 도식**이며 점퍼선의 실제 길이와 물리 배치를 정밀 실측한 도면은 아닙니다. 보유 LCD·가변저항은 V5에 아직 연결되지 않았습니다.

## Quick start / 설치 및 실행

### 1 — Upload Arduino firmware / 아두이노 업로드

Open [`arduino/ThreatTrack_V5/ThreatTrack_V5.ino`](arduino/ThreatTrack_V5/ThreatTrack_V5.ino) in Arduino IDE, select **Arduino Uno** and the correct COM port, then press **Upload**. / Arduino IDE에서 `.ino`를 열고 `Arduino Uno` 및 정확한 COM 포트를 선택해 업로드합니다.

### 2 — Install Python dependency / Python 라이브러리 설치

From the project root / 프로젝트 최상위 폴더에서:

```powershell
py -m pip install -r python/requirements.txt
```

### 3 — Identify port, launch / 포트 확인 및 실행

```powershell
py python/threat_track_dashboard.py --list-ports
py python/threat_track_dashboard.py --port COM5
```

**Close the Arduino Serial Monitor before opening the dashboard**. Only one application can control COM5 at a time. / **Python을 실행하기 전 Arduino 시리얼 모니터를 닫아야 합니다.** COM 포트는 다른 프로그램과 동시에 점유할 수 없습니다.

### Offline design preview / 센서 없이 UI 미리보기

```powershell
py python/threat_track_dashboard.py --demo
```

The demo mode displays **simulated values** and visibly labels them. / 데모 모드는 **가상 측정값**을 사용하며 화면에 시뮬레이션임을 표시합니다.

### Run tests / 코드 테스트

```powershell
py -m unittest discover -s tests -v
```

## Project status / 프로젝트 진행 상태

| Milestone | Status | Evidence / 설명 |
|---|---|---|
| Arduino UNO Blink | ✅ Confirmed / 확인 | Board LED flash validated during build |
| HC-SR04 range readings | ✅ Confirmed / 확인 | Actual serial-monitor photograph above |
| Three-state LED warnings | ✅ User-reported success / 성공 보고 | Red, yellow, green LEDs working |
| Buzzer audio alert | ✅ User-reported success / 성공 보고 | Audible buzzer working |
| Python GUI startup | ✅ User-reported success / 실행 보고 | Desktop interface opens |
| V5 live Arduino→Python telemetry | ⚠️ Pending re-verification / 재확인 필요 | An observed COM5 port collision blocked a firmware upload; live refresh not yet re-confirmed |
| LCD and potentiometer features | Not implemented / 미구현 | Future extension only |

## Troubleshooting / 문제 해결

**Problem / 문제: UI opens but numbers never change.** The Arduino firmware may be an older V4 format, or COM5 may still be held by Python/Arduino IDE. / 화면은 뜨지만 값이 바뀌지 않는 경우 구형 시리얼 형식이나 COM 포트 점유가 원인일 수 있습니다.

1. Close the Python window and its CMD process / Python 화면과 CMD 종료
2. Close Arduino Serial Monitor / 시리얼 모니터 닫기
3. Upload the V5 `.ino` again, and confirm **Done uploading** / V5 코드 다시 업로드 후 완료 확인
4. Temporarily open Serial Monitor at **9600 baud**; verify `23.4,42.8,0.55,DANGER`-style lines / 쉼표 4개 항목 형식 출력 확인
5. Close Serial Monitor, then run the dashboard / 시리얼 모니터 닫고 Python 실행

For an actual example of a COM5 conflict / 실제 포트 충돌 화면:

![Actual COM port upload error](assets/screenshots/com-port-error.jpg)

## Reproducibility, evaluation plan / 재현성과 후속 검증 설계

**Reproducibility / 재현:** Arduino firmware is versioned, serial packets are parsed and checked for malformed/out-of-range data, Python demo mode is explicitly separated from physical measurements, and charts are generated from tracked CSV data plus deterministic equations. / 펌웨어 버전을 관리하고, 패킷 파서에서 오염 데이터를 걸러내며, 시뮬레이션과 실측을 구분하고, CSV 및 계산식을 기반으로 그래프를 재생성합니다.

**Next controlled experiment / 다음 검증 실험:** Fix a flat target at known reference distances (e.g., 10–150 cm), collect repeated measurements and log timestamps; estimate bias, MAE, variation and invalid-echo fraction by distance; repeat controlled approach/retreat trajectories; measure warning response latency. These experiments are **proposed, not performed**. / 기준 거리를 고정한 반복 측정과 타임스탬프 기록을 추가해 편향, MAE, 분산, 무효 반사 비율, 경보 지연을 측정할 계획입니다. **아직 수행하지 않은 실험입니다.**

The GUI is an HMI prototype that favors separation of sensing, control, and display. The sweeping radar graphic is stylistic only and does not convey bearing information. / GUI는 센싱·제어·표시 계층을 분리한 HMI 실험이며, 레이더 회전 효과는 시각적 표현일 뿐 방위각을 측정하지 않습니다.

## Repository layout / 저장소 구조

```text
.
├── README.md
├── .github/workflows/quality.yml
├── arduino/ThreatTrack_V5/ThreatTrack_V5.ino
├── python/threat_track_dashboard.py
├── python/telemetry.py
├── python/requirements.txt
├── analysis/{generate_figures.py,requirements.txt}
├── data/serial_monitor_photo_readings.csv
├── assets/charts/{serial-readings-photo.png,alert-decision-map.png,ttc-model.png}
├── assets/diagrams/{wiring-cad.svg,wiring-cad.png,system-flow.svg,system-flow.png,buzzer-breadboard.svg,buzzer-breadboard.png}
├── assets/screenshots/{hardware-prototype.jpg,ultrasonic-wiring.jpg,serial-monitor.jpg,
│                     arduino-ide-code-photo.jpg,dashboard-demo-screenshot.png,com-port-error.jpg}
├── docs/cad/threat-track-schematic.dxf
└── tests/test_telemetry.py
```

## Engineering limitations / 기술적 한계

**EN:** This device estimates one-dimensional range, not object identity or direction. Moving hands and reflective surfaces cause noise, and TTC assumes constant relative speed. An animated radar sweep in the GUI is **purely stylistic**. No false-alarm rates, precision, or deployment performance are claimed without a controlled validation experiment. Not for real military, security, or collision-prevention use.

**KO:** 단일 센서로 측정하는 값은 정면 거리 하나이며 물체의 종류나 방향은 식별하지 못합니다. 손 움직임과 반사 표면 때문에 측정 오차가 발생하고 TTC는 접근 속도가 일정하다는 가정입니다. 화면의 레이더 회전 효과는 **시각적 연출**에 불과합니다. 검출 정확도·오경보율·실제 운용 성능은 검증 전까지 주장하지 않습니다. 실제 군사·보안·충돌 방지 용도로 사용하지 마세요.

## Author / 제작

**Doyun Shin · 신도윤**  
Gachon University · Industrial Engineering / 가천대학교 산업공학과  
Personal embedded-systems and human–machine interface portfolio / 개인 임베디드·인간–기계 인터페이스 프로젝트

**Asset provenance / 자료 출처:** [Full source and evidence disclosure](assets/ASSET_PROVENANCE.md) · [Wiring CAD notes](docs/cad/README.md)

**Asset note / 자료 고지:** Hardware and serial-monitor photographs were supplied during this project's build conversation. The CAD diagrams and GUI preview are authored technical illustrations; the GUI screenshot is from a real execution in explicitly labeled `--demo` mode and uses simulated telemetry, not a live sensor reading. / 사진은 제작 과정에서 제공된 실제 촬영 이미지이며, CAD와 관제 화면은 실행된 프로그램의 데모 모드 캡처이며 수치는 가상 데이터입니다.