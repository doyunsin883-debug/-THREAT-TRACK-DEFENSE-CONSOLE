# Reproducible validation plan / 재현 가능한 후속 검증 계획

**Status: proposed, NOT performed. / 상태: 설계 단계, 미실시.**  
This page sets up tests needed to turn a working demonstration into an evidence-based engineering portfolio. / 작동 시연을 정량 검증 연구로 확장하기 위한 계획이다.

## A. Distance accuracy / 거리 측정 정확도

Place a flat target at reference distances `10, 20, 30, 50, 70, 100, 150 cm`. Log at least 30 samples at each distance in the same room and record the ground-truth distance with a ruler/tape. Do not change the target orientation between repeats. / 평평한 표적을 기준 거리 7개에 고정하고, 각 지점에서 30회 이상 반복 측정한다. 줄자 측정 거리와 반사판 방향을 함께 기록한다.

Metrics: bias `mean(measured−reference)`, MAE, sample standard deviation, coefficient of variation where appropriate, and invalid echo rate. / 평가 지표: 편향, 평균절대오차, 표본표준편차, 무효 반사 비율 등.

## B. Speed and TTC / 속도·예상 접촉시간 검증

Move one large flat object along the sensor axis over repeated runs, capture timestamps and an independent reference trajectory (video with a ruler in frame or a calibrated linear motion guide). Compare finite-difference speed and TTC with reference estimates, and record motion direction. / 센서 정면에서 표적을 반복 이동시키고 타임스탬프 및 독립적인 기준 궤적을 기록해 속도·TTC 추정 오차를 비교한다.

Metric candidates: speed MAE, TTC absolute error for valid approaching samples, fraction of invalid TTC, and smoothing-induced delay. / 평가지표 후보: 속도 MAE, TTC 오차, 계산 불가 비율, 평활로 인한 지연.

## C. Alarm timeliness / 경보 적시성

Record range, TTC and LED state at the moment each threshold is crossed. Separately verify buzzer sound with independent audio recording. Compare warning-onset time against threshold-crossing time. / 경계 통과 시점과 LED 변경 시점을 기록하고, 부저는 별도 녹음으로 확인해 경보 지연을 계산한다.

## D. Human factors / 인간공학 평가

Measure whether the three states are recognized under ordinary viewing and listening conditions, with sufficient contrast and simple labels. Report experimental sample size and protocol before interpreting any percentages. / 3색 LED 및 부저 경고 패턴의 인지 용이성을 관찰하고, 참가자 수·실험 조건을 명시한 뒤 분석한다.

## E. Reproducibility and boundaries / 재현성·해석 범위

Save raw logs, timestamps, firmware version, COM port, power condition, environment temperature, and hardware connection map. Separate **observed hardware results**, **mathematical visualizations**, and **simulated interface demonstration** in figures and captions. / 원시 로그, 펌웨어 버전, 포트·전원·환경조건을 기록하고 **실험 관측값 / 계산식 기반 그래프 / 시뮬레이션 화면**을 구분한다.

No measured accuracy, reliability or safety figures are claimed until the experiment is actually conducted. / 실험 전에는 정확도, 신뢰도, 안전 성능 수치를 주장하지 않는다.
