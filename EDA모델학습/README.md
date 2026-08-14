# 데이터 EDA 및 모델 학습 — 학습 정리 세트

업로드한 `(실습-문제) 1-1_데이터 EDA 및 모델 학습.ipynb` · `(과제-문제) 1-1_데이터 EDA 및 모델 학습.ipynb`
두 파일의 내용을 학습용으로 재구성한 자료입니다.

## 파일

| 파일 | 내용 | 여는 법 |
|---|---|---|
| `20_EDA_모델학습_개념정리.html` | **개념 정리 본문** + 인터랙티브 실습 12개 + 그림 10장 | 더블클릭 (브라우저) |
| `21_실습_따라하기.ipynb` | 파이프라인 전 과정 코드 노트북 (55셀, 빈칸 없음) | Jupyter / VS Code |
| `22_문제집.ipynb` | 문제 58문항 (O/X 15 · 빈칸 12 · 계산 8 · 코드 12 · 디버깅 5 · 서술형 6) | Jupyter / VS Code |
| `23_해답.ipynb` | 정답 + 해설 + 모범답안 | Jupyter / VS Code |

## 다루는 범위

1. **ML 기초 개념** — AI/ML/DL, 지도/비지도학습, 과소·과대적합, Train/Valid/Test 분할
2. **EDA** — pandas 기초 통계, 상관관계와 히트맵(mask·annot·fmt·cmap), histplot 3종, scatterplot, pairplot
3. **결측치·이상치** — 결측 탐지/시각화, 평균·중앙값 대체, SimpleImputer, IQR 기반 이상치 탐지와 처리
4. **전처리** — train_test_split(test_size·random_state·stratify), StandardScaler, **데이터 누수(Leakage)**
5. **분류** — LogisticRegression, 혼동 행렬, precision/recall/F1, classification_report, ROC-AUC, 임계값
6. **회귀** — LinearRegression, RMSE·MAE·R², 잔차 플롯, 연속형 타깃 stratify(`pd.qcut`)
7. **검증·해석** — cross_val_score(K-Fold), PCA, KMeans, Pipeline

## HTML 안의 인터랙티브 실습 12개

1. 과소적합 ↔ 과대적합 직접 만들기 (차수 슬라이더 + 훈련/테스트 오차 곡선)
2. 분할 비율과 `stratify` 효과 (20번 반복해 흔들림 관찰)
3. 상관계수 $r$ 감 잡기 & 비선형의 함정 ($y=x^2$ 인데 $r\approx0$)
4. 결측치를 평균 vs 중앙값으로 채우면? (분포·표준편차 변화)
5. IQR 이상치 탐지기 (숫자를 직접 입력 → Q1·Q3·경계·boxplot)
6. **데이터 누수가 성능을 부풀리는 실험** (무작위 특성으로 정확도 0.5 → 0.66)
7. 임계값(threshold)을 움직이면 지표가 어떻게 변할까
8. ROC 곡선이 그려지는 과정 (임계값 점이 곡선 위를 이동)
9. 이상치 하나가 RMSE와 MAE에 미치는 영향
10. K-Fold 교차검증 시각화 (폴드 분할 + 각 fold 점수)
11. PCA가 찾는 축 직접 보기 (공분산 → 고유값 → PC1/PC2)
12. KMeans 반복 과정 한 스텝씩 (배정 ↔ 중심 이동)

## 문제집 특징

- 원본 SSAFY 실습 파일과 **같은 방식**(`# TODO` 채우고 `assert`로 자동 채점)
- **파트 E 디버깅**: 실무에서 가장 자주 나는 실수 5가지를 코드로 고쳐보는 문제
  (test로 `fit_transform`, 전체 스케일링 후 분할, 전처리 안 된 데이터로 `predict_proba`,
   test로 IQR 경계 계산, CV 전에 전체 스케일링)
- 파트 A~C는 `ANSWER_A/B/C` 딕셔너리에 답을 적고 채점 셀 실행 → 점수 자동 집계 (35점 만점)

## 필요 환경

```
pip install numpy pandas matplotlib seaborn scikit-learn jupyter
```

- 노트북은 **인터넷 없이도** 전부 동작합니다.
  (원본 과제의 Boston 데이터는 `fetch_openml` 다운로드가 필요해, 같은 구조의 합성 주택 데이터로 대체했습니다.
   실제 Boston을 쓰려면 `21_실습_따라하기.ipynb` Step 7의 주석 코드를 사용하세요.)
- HTML은 인터넷 연결 시 수식(MathJax)이 예쁘게 렌더링됩니다. 오프라인이면 LaTeX 원문으로 보입니다.

## 추천 학습 순서

`20_개념정리` 로 개념 잡고 실습 슬라이더 직접 만져보기 → `21_실습_따라하기` 로 코드 확인 →
`22_문제집` 풀고 채점 → `23_해답` 으로 확인
