# Stochastic Interest Rate Modelling and Prediction using the Cox-Ingersoll-Ross (CIR) Model

[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/Lakshya-24117068/Finance_Project_CIR_Yield_Curve_Modeling/workflows/Python%20application/badge.svg)](https://github.com/Lakshya-24117068/Finance_Project_CIR_Yield_Curve_Modeling/actions)

An end-to-end quantitative finance pipeline implementing, calibrating, and backtesting the Cox-Ingersoll-Ross (CIR) short-rate model, along with advanced extensions (CIR++ and Jump-Diffusion) to reconstruct the zero-coupon yield curve.

---

## 1. Project Overview

This repository provides a production-grade codebase for stochastic interest rate modelling. The core objective is to reconstruct the entire yield curve (6 Months through 30 Years) from a single observable input—the **3-Month yield**—acting as a proxy for the instantaneous short rate $r_t$.

The pipeline contains:
- A data preprocessing package including outlier smoothing (Z-score and IQR-based), duplicate removal, and date validation.
- Standard short-rate calibrations: Time-Series Ordinary Least Squares (OLS), Maximum Likelihood Estimation (MLE), and Generalized Method of Moments (GMM).
- Zero-coupon bond pricing under the standard CIR framework and its extensions.
- Advanced model extensions: Jump-Diffusion CIR (Poisson jumps) and CIR++ (time-dependent deterministic shifts).
- Out-of-sample backtesting metrics ($R^2$, adjusted $R^2$, RMSE, MAE, MAPE).
- Publication-quality Jupyter Research Notebooks.

---

## 2. Mathematical Background

### The Cox-Ingersoll-Ross (CIR) Model
The instantaneous short rate $r_t$ evolves according to the stochastic differential equation:
$$dr_t = \kappa(\theta - r_t) dt + \sigma \sqrt{r_t} dW_t$$
where $\kappa$ is the mean reversion speed, $\theta$ is the long-run mean, $\sigma$ is the volatility coefficient, and $W_t$ is standard Brownian motion.
The square-root term guarantees non-negativity under the **Feller Condition**:
$$2\kappa\theta \ge \sigma^2$$

### Analytical Pricing
The zero-coupon yield for maturity $\tau = T - t$ is given by:
$$y(t, \tau) = \frac{B(t, \tau) r_t - \ln A(t, \tau)}{\tau}$$
where:
$$h = \sqrt{\kappa^2 + 2\sigma^2}$$
$$A(t, \tau) = \left[ \frac{2 h e^{(h + \kappa)\tau/2}}{(h + \kappa)(e^{h\tau} - 1) + 2h} \right]^{\frac{2\kappa\theta}{\sigma^2}}$$
$$B(t, \tau) = \frac{2(e^{h\tau} - 1)}{(h + \kappa)(e^{h\tau} - 1) + 2h}$$

---

## 3. Repository Structure

```
Finance_Project/
├── README.md
├── requirements.txt
├── setup.py

├── notebooks/
│   ├── Stochastic_Interest_Rate_Modelling.ipynb

                
```

---

## 4. Installation

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/Lakshya-24117068/Finance_Project_CIR_Yield_Curve_Modeling.git
cd Finance_Project_CIR_Yield_Curve_Modeling
pip install -r requirements.txt
pip install -e .
```

---

## 5. Usage

### Preprocessing & Data Cleaning
Run the data cleaning pipeline to generate smoothed datasets:
```python
from src.data.loader import DataLoader
from src.data.cleaner import DataCleaner

loader = DataLoader()
df_raw = loader.load_raw_data("train_data.csv")

cleaner = DataCleaner()
df_cleaned = cleaner.clean(df_raw)

loader.save_processed_data(df_cleaned, "train_data.csv")
```

### Running Model Calibration & Backtests
Execute the calibration and evaluation routines:
```python
import numpy as np
from src.data.loader import DataLoader
from src.calibration.mle import MLECalibrator
from src.pricing.bond_pricing import CIRBondPricer
from src.evaluation.backtesting import YieldCurveBacktester

loader = DataLoader()
train_df = loader.load_processed_data("train_data.csv")
test_df = loader.load_processed_data("test_data.csv")

# Calibrate parameters using Maximum Likelihood
rt = train_df['ZC025YR'].values
mle = MLECalibrator()
kappa, theta, sigma = mle.calibrate(rt)

# Run out-of-sample backtest
pricer = CIRBondPricer(kappa, theta, sigma)
backtester = YieldCurveBacktester(pricer)

maturities = {'ZC050YR': 0.50, 'ZC100YR': 1.00, 'ZC200YR': 2.00}
r2, results = backtester.backtest(test_df, maturities)
print(f"Out-of-sample R2: {r2:.4f}")
```

### Running the Unit Tests
Validate that all math models, loader functions, and pricing engines are functional:
```bash
pytest
```

---

## 6. Results & Insights

- **Calibration Performance**: Time-series OLS estimates $\kappa < 0$ because daily fluctuations in interest rates are highly noisy. Cross-sectional optimization resolves this, providing positive parameter estimates ($\kappa = 0.166295$) that satisfy the Feller Condition.
- **Predictive Accuracy**: Utilizing the 3M yield as $r_t$, the model reconstructs the out-of-sample yield curve (6M, 9M, 1Y, 2Y) with an **overall $R^2$ score of 0.8938**, outperforming the 0.85 evaluation benchmark.
- **Yield Inversion Bias**: The model exhibits a systematic overestimation bias (mean bias ~ -0.00077) during the test period (2024-2026). This is because the test period features a deeply inverted yield curve where short rates are high but long-term yields drop rapidly, which cannot be fully anticipated by a single-factor constant-parameter model.

---

## 7. Future Improvements
- **Multi-Factor CIR Models**: Incorporate a second independent factor to capture slope/curvature changes of the yield curve.
- **Kalman Filtering**: Implement a state-space filter to treat the short rate as a latent variable rather than proxying it directly with the 3M rate.

---

## 8. References
1. Cox, J. C., Ingersoll, J. E., & Ross, S. A. (1985). *A Theory of the Term Structure of Interest Rates*. Econometrica, 53(2), 385-407.
2. Duffie, D., Pan, J., & Singleton, K. (2000). *Transform Analysis and Asset Pricing for Affine Jump-Diffusions*. Econometrica, 68(6), 1343-1376.
3. Brigo, D., & Mercurio, F. (2006). *Interest Rate Models - Theory and Practice: With Smile, Inflation and Credit*. Springer Finance.
