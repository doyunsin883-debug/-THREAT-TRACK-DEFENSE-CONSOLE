# Asset provenance / 촬영·제작 기록 출처

**EN:** I distinguish original hardware/IDE photography, reproducible analytical plots, technical diagrams and an executed demo-mode UI screenshot. These sources have different evidentiary meanings.

**KO:** 직접 촬영한 하드웨어·개발 화면, 계산식 기반 그래프, CAD 기술 도면, 데모 모드로 실행한 Python GUI 화면을 구분해 정리했다. 실제 측정·이론적 시각화·시뮬레이션은 서로 다른 증거다.

| Asset | Source | Claim |
|---|---|---|
| `screenshots/hardware-prototype.jpg` | My original build photograph / 제작 과정 직접 촬영 | Physical assembly during build; not necessarily final 3-LED state |
| `screenshots/ultrasonic-wiring.jpg` | My original build photograph / 제작 과정 직접 촬영 | Early HC-SR04 wiring |
| `screenshots/serial-monitor.jpg` | My original build photograph / 제작 과정 직접 촬영 | Eight actual visible distance readings |
| `screenshots/arduino-ide-code-photo.jpg` | Crop of my Arduino IDE photo / 직접 촬영한 코드 화면 일부 | CSV output firmware shown during failed COM5 upload; not proof upload succeeded |
| `screenshots/com-port-error.jpg` | My original build photograph / 제작 과정 직접 촬영 | Actual COM5 conflict / 업로드 오류 |
| `screenshots/dashboard-demo-screenshot.png` | Screenshot of executed Python Tkinter program in `--demo` mode / 실행 화면 캡처 | Simulated values only, not live telemetry |
| `diagrams/*.svg`, `diagrams/*.png` | Authored technical vector diagrams / 직접 제작 기술 도식 | Connections based on V5 sketch; not precise 1:1 board CAD |
| `charts/serial-readings-photo.png` | Matplotlib plotting from CSV transcription of photographed values / 실제 사진에서 전사 | 8 readings; no timestamps, calibration, ground-truth |
| `charts/alert-decision-map.png` | Matplotlib deterministic policy visualization | Not a measured accuracy result |
| `charts/ttc-model.png` | Matplotlib deterministic model visualization | Not a measured TTC result |

**No generative-AI artwork is embedded. / AI 생성 미술 이미지 없음.**
