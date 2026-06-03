# Mathematical Theory of Stochastic Interest Rates

This document outlines the stochastic calculus foundations and short-rate models used in this project.

## 1. Stochastic Calculus & Brownian Motion
A stochastic process $W_t$ is a standard **Brownian Motion** (or Wiener process) if:
1. $W_0 = 0$
2. It has independent increments: for $t > s$, $W_t - W_s$ is independent of the process history up to time $s$.
3. The increments are normally distributed: $W_t - W_s \sim N(0, t - s)$.
4. The paths $t \mapsto W_t$ are almost surely continuous.

### Ito's Lemma
For a stochastic process $X_t$ governed by the SDE:
$$dX_t = \mu(X_t, t) dt + \sigma(X_t, t) dW_t$$
and a twice-differentiable function $g(X_t, t)$, the differential $dg(X_t, t)$ is given by:
$$dg(X_t, t) = \left( \frac{\partial g}{\partial t} + \mu(X_t, t) \frac{\partial g}{\partial X} + \frac{1}{2} \sigma(X_t, t)^2 \frac{\partial^2 g}{\partial X^2} \right) dt + \sigma(X_t, t) \frac{\partial g}{\partial X} dW_t$$

---

## 2. Short Rate Modelling
A short-rate model describes the dynamics of the instantaneous interest rate $r_t$. The price of a Zero-Coupon Bond (ZCB) maturing at time $T$ is given under the risk-neutral probability measure $\mathbb{Q}$ by:
$$P(t, T) = \mathbb{E}_t^{\mathbb{Q}} \left[ \exp \left( -\int_t^T r_s ds \right) \right]$$

### The Vasicek Model
Introduced in 1977, the Vasicek model assumes:
$$dr_t = \kappa(\theta - r_t) dt + \sigma dW_t$$
where $\kappa$ is the speed of mean reversion, $\theta$ is the long-run mean, and $\sigma$ is constant volatility.
- **Drawback**: Interest rates can become negative with positive probability because the volatility term does not depend on the level of the interest rate.

### The Cox-Ingersoll-Ross (CIR) Model
Introduced in 1985, the CIR model addresses the positivity issue:
$$dr_t = \kappa(\theta - r_t) dt + \sigma \sqrt{r_t} dW_t$$
The square-root diffusion term $\sigma \sqrt{r_t}$ scales volatility with the interest rate level. As $r_t \to 0$, volatility vanishes, and the positive drift $\kappa\theta dt$ pulls the rate back toward $\theta$, ensuring non-negativity.

### The Feller Condition
To guarantee that the short rate $r_t$ remains strictly positive and never touches zero, the parameters must satisfy:
$$2\kappa\theta \ge \sigma^2$$
If this condition is violated, the boundary $r_t = 0$ is attainable, though it acts as a reflecting boundary (rates cannot cross below zero).
