# ACC Simulation with PID and ML Imitation Learning

Adaptive Cruise Control (ACC) 시뮬레이션 프로젝트입니다.  
PID 기반 ACC 제어기를 기준 정책(Teacher)으로 설정하고,  
시뮬레이션 로그를 활용해 Machine Learning 기반 가속도 제어기(Student)를 학습 및 검증합니다.

본 프로젝트의 핵심 목표는  
Rule-based PID 제어기를 데이터 기반 제어기로 대체할 수 있는 가능성을 실험적으로 확인하는 것입니다.

---

## 1. Project Overview

본 프로젝트는 단순화된 ACC 시뮬레이션 환경에서 다음 과정을 수행합니다.

1. PID 기반 ACC 제어기 구현
2. 다양한 시나리오에서 시뮬레이션 수행
3. PID 제어기의 가속도 명령을 데이터로 수집
4. Machine Learning 모델을 이용한 PID 정책 모사 (Imitation Learning)
5. ML 기반 ACC 제어기를 시뮬레이터에 직접 적용
6. PID와 ML 제어기의 주행 성능 비교

---

## 2. Core Concept

PID 제어기를 기준 정책으로 설정하고,  
해당 제어기의 행동을 ML 모델이 학습하도록 구성합니다.

# ACC Simulation with PID and ML Imitation Learning

Adaptive Cruise Control (ACC) 시뮬레이션 프로젝트입니다.  
PID 기반 ACC 제어기를 기준 정책(Teacher)으로 설정하고,  
시뮬레이션 로그를 활용해 Machine Learning 기반 가속도 제어기(Student)를 학습 및 검증합니다.

본 프로젝트의 핵심 목표는  
Rule-based PID 제어기를 데이터 기반 제어기로 대체할 수 있는 가능성을 실험적으로 확인하는 것입니다.

---

## 1. Project Overview

본 프로젝트는 단순화된 ACC 시뮬레이션 환경에서 다음 과정을 수행합니다.

1. PID 기반 ACC 제어기 구현
2. 다양한 시나리오에서 시뮬레이션 수행
3. PID 제어기의 가속도 명령을 데이터로 수집
4. Machine Learning 모델을 이용한 PID 정책 모사 (Imitation Learning)
5. ML 기반 ACC 제어기를 시뮬레이터에 직접 적용
6. PID와 ML 제어기의 주행 성능 비교

---

## 2. Core Concept

PID 제어기를 기준 정책으로 설정하고,  
해당 제어기의 행동을 ML 모델이 학습하도록 구성합니다.
PID Controller (Teacher)
↓
Simulation Log (state → accel)
↓
ML Regression Model
↓
ML-based ACC Controller


---

## 3. Project Structure

acc_sim/
├── data/
│ └── ml_dataset.csv
│
├── notebooks/
│ ├── eda.ipynb
│ └── analysis.ipynb
│
├── results/
│ ├── acc_log.csv
│ └── pid_best_result.csv
│
├── src/
│ ├── adas/
│ │ └── pid_acc.py
│ │
│ ├── sim/
│ │ └── world.py
│ │
│ ├── vehicle/
│ │ └── model.py
│ │
│ ├── experiments/
│ │ └── runner.py
│ │
│ └── ml/
│ ├── generate_ml_dataset.py
│ ├── train_ml_accel.py
│ └── ml_acc_controller.py
│
├── main.py
├── requirements.txt
└── README.md


---

## 4. Simulation Environment

### Vehicle Model
- 1D longitudinal motion
- Discrete-time simulation

### State Variables
- Ego vehicle speed
- Lead vehicle speed
- Relative distance
- Relative speed
- Time headway

### Control Objective
- Maintain target time headway
- Avoid excessive acceleration and deceleration

---

## 5. PID-based ACC Controller

PID 기반 ACC 제어기는 다음 요소를 사용해 가속도를 계산합니다.

- Time headway error
- Integral term
- Derivative term
- Acceleration saturation (physical constraint)

PID 제어기는 안정적인 기준 정책으로 사용되며,  
ML 학습을 위한 Teacher 역할을 수행합니다.

---

## 6. ML Dataset Generation

PID 기반 시뮬레이션을 다양한 초기 조건에서 반복 실행하여  
ML 학습용 데이터셋을 생성합니다.

### Input Features
- ego_speed
- lead_speed
- distance
- relative_speed
- time_headway

### Target
- accel (PID controller output)

실행 방법:

```bash
python -m src.ml.generate_ml_dataset
## 7. ML-based ACC (Imitation Learning)
-Training

-Supervised regression

-Target: PID-generated acceleration

-Model: RandomForestRegressor

-python -m src.ml.train_ml_accel


-ML 모델은 PID 제어 정책을 근사하여
-PID 없이도 유사한 가속도 명령을 생성하는 것을 목표로 합니다.

## 8. Applying ML Controller to Simulation (STEP 1)

ML 기반 ACC 제어기는 PID 제어기와 동일한 인터페이스를 가지도록 구현되어,
시뮬레이션 엔진에 직접 교체 적용이 가능합니다.

controller = MLACCController("models/ml_accel_model.pkl")
df = run_simulation(controller, scenario)


PID 코드 수정 없이 Controller 교체만으로 실험이 가능합니다.

9. PID vs ML Performance Comparison

다음 항목을 중심으로 성능을 비교합니다.

Acceleration tracking

Time headway maintenance

Stability and smoothness of acceleration

실험 결과, ML 기반 ACC는 PID 가속도를 높은 정확도로 근사하며
일부 구간에서는 더 부드러운 가속 특성을 보입니다.

10. Future Work

PID and ML hybrid controller with fallback logic

Feature importance analysis for controller interpretation

Neural Network based ACC controller

Extended driving scenarios (cut-in, stop-and-go)

Reward-based learning approach

11. Requirements
Python >= 3.10
numpy
pandas
matplotlib
seaborn
scikit-learn


설치:

pip install -r requirements.txt

12. Summary

본 프로젝트는 제어 이론 기반 접근과 데이터 기반 접근을 결합하여
ACC 시스템을 설계하고 검증하는 것을 목표로 합니다.

PID 제어기를 기준 정책으로 설정하고,
해당 정책을 ML 모델이 학습하여
데이터 기반 제어기로의 전환 가능성을 실험적으로 확인합니다.
