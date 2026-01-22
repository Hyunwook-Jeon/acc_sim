# Adaptive Cruise Control (ACC) Simulation Project

이 저장소는 Adaptive Cruise Control (ACC) 알고리즘을 시뮬레이션으로 구현하고,
PID 기반 제어기와 Machine Learning 기반 제어기를 비교·확장하는 프로젝트입니다.

PID 제어기를 기준 정책(Teacher)으로 설정하고,
시뮬레이션 로그를 활용해 ML 모델이 가속도 명령을 학습하는
Imitation Learning 구조를 실험합니다.

---

## 🧠Project Overview(프로젝트 개요)

본 프로젝트에서는 다음 과정을 수행합니다.

1. PID 기반 ACC 제어기 구현
2. 시뮬레이션 환경에서 차량 종방향 거동 모델링
3. PID 제어기의 가속도 명령 로그 수집
4. ML 회귀 모델을 이용한 PID 정책 모사
5. ML 기반 ACC 제어기를 시뮬레이터에 직접 적용
6. PID vs ML 주행 성능 비교

---

## Core Concept

PID Controller (Teacher)
        ↓
Simulation Log (state → accel)
        ↓
ML Regression Model
        ↓
ML-based ACC Controller

---

## 📁Project Structure

acc_sim/

├── data/

│   └── ml_dataset.csv

├── notebooks/

│   ├── eda.ipynb

│   └── analysis.ipynb

├── results/

│   ├── acc_log.csv

│   └── pid_best_result.csv

├── src/

│   ├── adas/

│   │   └── pid_acc.py

│   ├── sim/

│   │   └── world.py

│   ├── vehicle/

│   │   └── model.py

│   ├── experiments/

│   │   └── runner.py

│   └── ml/

│       ├── generate_ml_dataset.py

│       └── ml_acc_controller.py

├── main.py

├── requirements.txt

└── README.md

---

## 📊 Results & Analysis Files

### 결과 CSV 위치

- PID Gain Sweep 결과: `results/pid_gain_sweep.csv`
  - 컬럼: `kp, ki, kd, mean_th_error`
- 시뮬레이션 로그: `results/pid_tuning_result.csv`
  - 컬럼: `time, ego_speed, lead_speed, distance, time_headway, accel`

### 분석 스크립트

- Gain Sweep Heatmap: `python -m src.analysis.visualize_pid`
- Best/Worst Gain 비교: `python -m src.analysis.compare_pid`
- 시뮬 로그 성능 Plot: `python -m src.analysis.plot_pid_results`


## ⚙️ 설치 및 실행

먼저 의존성 설치:

```bash
pip install -r requirements.txt
```
---

## Simulation Environment

- 1D longitudinal vehicle dynamics
- Discrete-time simulation
- Time headway based control objective

---

## PID-based ACC Controller

PID 기반 ACC 제어기는 Time Headway 오차를 기반으로
가속도 명령을 계산합니다.
- Proportional / Integral / Derivative term
- Acceleration saturation 적용
- 안정적인 기준 정책 역할 수행
해당 제어기는 ML 학습을 위한 기준 정책(Teacher)으로 사용됩니다.

### 1) PID 기반 ACC 실행

main.py 에서 PID 기반 ACC 성능 비교 및 Gain Sweep 자동 실험이 가능합니다.
```bash
python -m src.main
```

### 2) PID 자동실험(Gain Sweep)

PID 기반 주행 로그를 수집하여 Machine Learning 학습용 데이터셋을 생성합니다.
```bash
python -m src.experiments.pid_gain_sweep
```


---

## ML Dataset Generation

PID 기반 시뮬레이션을 다양한 초기 조건에서 실행하여
ML 학습용 데이터셋을 생성합니다.

Input:
- ego_speed
- lead_speed
- distance
- relative_speed
- time_headway

Target:
- accel (PID output)

실행:

```bash
python -m src.ml.generate_ml_dataset
```

생성된 data/ml_dataset.csv 는 다음 컬럼을 갖습니다:

```bash
time,ego_speed,lead_speed,distance,
relative_speed,time_headway,accel
```

---

## ML-based ACC (Imitation Learning)

PID 제어기의 가속도 출력을 타깃으로 하는
Supervised Regression 문제로 정의합니다.
ML-based ACC (Imitation Learning)

PID가 생성한 가속도 명령을 타깃으로 하는
Supervised Regression 문제로 정의합니다.

- Model: RandomForestRegressor

- Input: vehicle state

- Output: acceleration

### ML 모델 학습 및 저장

`data/ml_dataset.csv`를 이용해 모델을 학습하고
`models/ml_accel_model.pkl`에 저장합니다.

```bash
python -m src.ml.train_ml_model
```



---

## PID vs ML Comparison

ML 기반 ACC는 PID 제어기의 가속 행동을 높은 정확도로 근사하며,
일부 상황에서는 더 부드러운 가속 특성을 보입니다.

ML 모델을 PID 대신 시뮬에 넣어서 직접 시뮬레이션을 수행할 수 있습니다:

```bash
from src.ml.ml_acc_controller import MLACCController
from src.experiments.runner import run_simulation

controller = MLACCController("models/ml_accel_model.pkl")
scenario = {
    "ego_init_speed": 20,
    "lead_init_speed": 15,
    "initial_gap": 30
}
df = run_simulation(controller, scenario)
```

또는 준비된 실행 스크립트를 사용할 수 있습니다:

```bash
python -m src.experiments.run_ml_acc
```

---


## Requirements

Python >= 3.10

numpy  
pandas  
matplotlib  
seaborn  
scikit-learn  
``` bash
pip install -r requirements.txt
```
---

## Summary

본 프로젝트는 제어 이론과 데이터 기반 접근을 결합하여
ACC 시스템의 확장 가능성을 탐구합니다.
