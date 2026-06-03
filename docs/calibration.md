# Calibration Methodologies for the CIR Model

This document describes the three methodologies implemented for parameter estimation.

## 1. Ordinary Least Squares (OLS)
Applying the Euler discretization to the CIR SDE:
$$r_{t+1} - r_t = \kappa(\theta - r_t) \Delta t + \sigma \sqrt{r_t} \epsilon_t \sqrt{\Delta t}$$
where $\epsilon_t \sim N(0, 1)$. Dividing by $\sqrt{r_t}$ to stabilize the variance:
$$\frac{r_{t+1} - r_t}{\sqrt{r_t}} = \frac{\kappa\theta\Delta t}{\sqrt{r_t}} - \kappa\sqrt{r_t}\Delta t + \sigma \sqrt{\Delta t} \epsilon_t$$
Let $Y_t = \frac{r_{t+1} - r_t}{\sqrt{r_t}}$, $X_{1,t} = \frac{\Delta t}{\sqrt{r_t}}$, and $X_{2,t} = -\sqrt{r_t}\Delta t$. This yields a linear regression model without intercept:
$$Y_t = \beta_1 X_{1,t} + \beta_2 X_{2,t} + \eta_t$$
From the estimated coefficients $\hat{\beta}_1$ and $\hat{\beta}_2$:
$$\kappa = \hat{\beta}_2, \quad \theta = \frac{\hat{\beta}_1}{\hat{\beta}_2}$$
$$\sigma = \sqrt{\frac{\text{Var}(\eta_t)}{\Delta t}}$$

---

## 2. Maximum Likelihood Estimation (MLE)
The transition probability density function of $r_{t}$ given $r_{t-\Delta t}$ has a closed-form expression based on the non-central chi-squared distribution:
$$f(r_t | r_{t-\Delta t}; \kappa, \theta, \sigma) = 2c \, f_{\chi^2_d(\lambda_c)}(2 c r_t)$$
where:
$$c = \frac{2 \kappa}{\sigma^2 (1 - e^{-\kappa \Delta t})}$$
$$d = \frac{4 \kappa \theta}{\sigma^2}$$
$$\lambda_c = 2 c r_{t-\Delta t} e^{-\kappa \Delta t}$$
The log-likelihood function to be maximized is:
$$\mathcal{L}(\kappa, \theta, \sigma) = \sum_{t=1}^{N-1} \ln f(r_{t+1} | r_t; \kappa, \theta, \sigma)$$

---

## 3. Generalized Method of Moments (GMM)
GMM uses conditional moment conditions. The conditional mean and variance under CIR are:
$$E[r_{t+1} | r_t] = r_t e^{-\kappa \Delta t} + \theta (1 - e^{-\kappa \Delta t})$$
$$\text{Var}(r_{t+1} | r_t) = r_t \frac{\sigma^2}{\kappa} (e^{-\kappa \Delta t} - e^{-2\kappa \Delta t}) + \theta \frac{\sigma^2}{2\kappa} (1 - e^{-\kappa \Delta t})^2$$
We define errors:
$$e_{1,t} = r_{t+1} - E[r_{t+1} | r_t]$$
$$e_{2,t} = e_{1,t}^2 - \text{Var}(r_{t+1} | r_t)$$
We use instruments $1$ and $r_t$ to form 4 moment conditions:
$$g(\Phi) = \frac{1}{M} \sum_{t} \begin{bmatrix} e_{1,t} \\ e_{1,t} \cdot r_t \\ e_{2,t} \\ e_{2,t} \cdot r_t \end{bmatrix}$$
The GMM estimator minimizes $g(\Phi)^T W g(\Phi)$ where $W$ is the identity matrix.
