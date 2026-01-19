📘 ACC Simulation with PID & ML Imitation Learning

Adaptive Cruise Control (ACC) simulation project
PID 기반 제어기를 기준 정책(Teacher)으로 설정하고,
시뮬레이션 로그를 활용해 Machine Learning 기반 가속도 제어기(Student) 를 학습 및 검증하는 프로젝트입니다.

1. 프로젝트 개요

본 프로젝트는 Adaptive Cruise Control (ACC) 시스템을 단순화한 시뮬레이션 환경에서,

PID 제어기의 동작을 명확히 이해하고

해당 제어 정책을 데이터로 수집한 뒤

Machine Learning 모델이 PID 제어기를 모사(imitation) 할 수 있는지 검증하는 것을 목표로 합니다.

궁극적으로는

Rule-based PID → Data-driven Controller
로의 전환 가능성을 실험적으로 확인합니다.

2. 핵심 아이디어
PID Controller (Teacher)
        ↓
Simulation Log (state → accel)
        ↓
ML Regression Model
        ↓
ML-based ACC Controller


PID 제어기는 baseline / reference policy

ML 모델은 PID가 만든 가속도 명령을 학습

동일 시나리오에서 PID vs ML 주행 성능 비교

3. 프로젝트 구조
acc_sim/
├── data/
│   └── ml_dataset.csv          # PID 시뮬 로그 기반 ML 데이터셋
│
├── notebooks/
│   ├── eda.ipynb               # 데이터 분석 및 시각화
│   └── analysis.ipynb
│
├── results/
│   ├── acc_log.csv
│   └── pid_best_result.csv
│
├── src/
│   ├── adas/
│   │   └── pid_acc.py          # PID 기반 ACC 제어기
│   │
│   ├── sim/
│   │   └── world.py            # 시뮬레이션 환경
│   │
│   ├── vehicle/
│   │   └── model.py            # 차량 동역학 모델
│   │
│   ├── experiments/
│   │   └── runner.py           # 공용 시뮬레이션 실행 엔진
│   │
│   └── ml/
│       ├── generate_ml_dataset.py  # ML 학습용 데이터 생성
│       ├── train_ml_accel.py       # ML 가속도 회귀 모델 학습
│       └── ml_acc_controller.py    # ML 기반 ACC Controller
│
├── main.py                      # PID 기반 시뮬 및 Gain Sweep
├── requirements.txt
└── README.md

4. 시뮬레이션 환경
차량 모델

1D longitudinal motion

상태 변수:

ego speed

lead speed

relative distance

time headway

ACC 제어 목표

목표 Time Headway 유지

과도한 가속/감속 방지

5. PID 기반 ACC

PID 제어기는 다음 항목을 기반으로 가속도를 계산합니다.

Time Headway error

Integral / Derivative term

가속도 saturation 적용 (물리적 제약)

PID 제어기는:

안정적인 baseline 제공

ML 학습을 위한 Teacher 역할 수행

6. ML 데이터셋 생성

PID 기반 시뮬레이션을 다양한 초기 조건에서 반복 실행하여
아래 형태의 데이터셋을 생성합니다.

입력 (State)

ego_speed

lead_speed

distance

relative_speed

time_headway

출력 (Target)

accel (PID가 계산한 가속도)

python -m src.ml.generate_ml_dataset

7. ML 기반 ACC (Imitation Learning)
학습 방식

Supervised Regression

PID 가속도 명령을 target으로 설정

RandomForest 기반 회귀 모델 사용

python -m src.ml.train_ml_accel

목표

ML 모델이 PID 제어 정책을 근사하여
PID 없이도 안정적인 ACC 주행이 가능한지 검증

8. ML Controller 시뮬 적용 (STEP 1)

ML 모델은 PID와 동일한 인터페이스를 가지는
MLACCController 형태로 구현되어,
기존 시뮬레이션 엔진(runner.py)에 그대로 교체 가능합니다.

controller = MLACCController("models/ml_accel_model.pkl")
df = run_simulation(controller, scenario)


PID 코드 수정 없음

Controller 교체만으로 실험 가능

9. PID vs ML 성능 비교

비교 항목:

가속도 추종 성능

Time Headway 유지 능력

가속도 안정성 (oscillation, jerk)

ML 모델은:

PID 가속도를 높은 정확도로 근사

일부 구간에서 더 부드러운 가속 특성 확인

10. 향후 발전 방향

PID + ML Hybrid Controller (fallback 구조)

Feature importance 기반 제어 해석

Neural Network 기반 ACC Controller

다양한 주행 시나리오 확장 (cut-in, stop-and-go)

Reward 기반 학습으로 확장 (RL 접근)

11. 실행 환경
Python >= 3.10
numpy
pandas
matplotlib
seaborn
scikit-learn

pip install -r requirements.txt

12. 프로젝트 의의

본 프로젝트는 단순한 ML 예제가 아니라,

제어 시스템 관점

데이터 기반 접근

시뮬레이션 중심 검증

을 결합한 ADAS / ACC 포트폴리오 프로젝트를 목표로 합니다.