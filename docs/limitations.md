# Practical Limitations & Market Dynamics

This document details the critical challenges faced by short-rate models in real-world application.

## 1. Single-Factor Structure & Yield Curve Shapes
Because the base CIR model is a single-factor model, all yields are perfectly correlated with the instantaneous short rate $r_t$.
- **Limitations**: A single-factor model cannot capture complex shape shifts in the yield curve, such as twists (changes in slope) or butterfly movements (changes in curvature). It constrains the yield curve to a narrow family of shapes (upward, downward, or humped).

## 2. Parameter Instability & Regime Shifts
Interest rates undergo regime shifts due to changing monetary policies, inflation targets, or economic cycles.
- **Example**: In our dataset, the training set represents a low-interest-rate environment (mean 3M yield ~1.67%) with a normal upward-sloping curve. The test set represents a high-interest-rate environment (mean 3M yield ~4.91%) with a deeply inverted curve.
- **Result**: A model calibrated on the training set has parameters geared toward low rates. When applied to the high-rate test period, it systematically overestimates yields because it expects rates to revert back to the training set's long-run mean $\theta = 2.44\%$, whereas the market has priced in a structural expectation of rate cuts.

## 3. The Feller Condition in Low-Rate Regimes
In low-rate regimes (where $\theta \to 0$) or when volatility $\sigma$ is high, the Feller condition $2\kappa\theta \ge \sigma^2$ is easily violated.
- **Consequence**: When $r_t$ reaches zero, numerical implementations of Euler schemes can yield negative values. The square root of negative numbers generates imaginary values and NaNs in simulations. Truncation or reflection methods are mandatory, but they introduce statistical bias.
