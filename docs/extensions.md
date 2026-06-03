# Advanced Model Extensions

This document explains the mathematical foundations of the implemented extensions.

## 1. CIR++ Model
The CIR++ model adds a deterministic shift function $\varphi(t)$ to the standard CIR process $x_t$:
$$r_t = x_t + \varphi(t)$$
where $x_t$ is a CIR process:
$$dx_t = \kappa(\theta - x_t)dt + \sigma \sqrt{x_t} dW_t$$
The pricing of zero-coupon bonds under CIR++ is:
$$P(t, T) = P^M(0, T) \frac{A(t, T; x_t) e^{-B(t, T) x_t}}{P^M(0, t) A(0, t; x_0) e^{-B(0, t) x_0}}$$
We calibrate $\varphi(\tau)$ for each maturity tenor $\tau$ as the average error between the market yields and the base CIR model predictions on the training dataset.

---

## 2. Two-Factor CIR Model
A Two-Factor CIR model assumes the short rate is the sum of two independent CIR processes:
$$r_t = x_{1,t} + x_{2,t}$$
$$dx_{j,t} = \kappa_j(\theta_j - x_{j,t}) dt + \sigma_j \sqrt{x_{j,t}} dW_{j,t}$$
The ZCB price is:
$$P(t, T) = P_1(t, T) P_2(t, T) = A_1(t, T)e^{-B_1(t, T)x_{1,t}} A_2(t, T)e^{-B_2(t, T)x_{2,t}}$$
Yield reconstruction uses the sum of the pricing components.

---

## 3. Jump-Diffusion CIR Model
The Jump-Diffusion CIR model incorporates Poisson jumps:
$$dr_t = \kappa(\theta - r_t) dt + \sigma \sqrt{r_t} dW_t + dJ_t$$
where jumps arrive at intensity $\lambda$ and jump sizes are exponentially distributed with mean $\mu_J$.
The log-A pricing coefficient is adjusted:
$$\ln A_{jump}(t, \tau) = \ln A_{base}(t, \tau) - \lambda \int_0^\tau \frac{\mu_J B(s)}{1 - \mu_J B(s)} ds$$
We evaluate the integral numerically using the trapezoidal rule.
