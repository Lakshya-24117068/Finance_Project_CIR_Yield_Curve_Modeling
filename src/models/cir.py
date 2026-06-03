import numpy as np
from typing import Tuple

class CIRModel:
    def __init__(self, kappa: float = 0.1, theta: float = 0.02, sigma: float = 0.05):
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma

    def update_params(self, kappa: float, theta: float, sigma: float) -> None:
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma

    def verify_feller(self) -> bool:
        """Checks Feller condition: 2 * kappa * theta >= sigma^2."""
        return 2 * self.kappa * self.theta >= self.sigma**2

    def simulate_euler(self, r0: float, T: float, steps: int, paths: int = 1) -> np.ndarray:
        """
        Simulates interest rate paths using Euler discretization.
        Guarantees positivity by using absorption: max(r_t, 0).
        """
        dt = T / steps
        r = np.zeros((steps + 1, paths))
        r[0, :] = r0
        
        for t in range(1, steps + 1):
            rt_prev = r[t-1, :]
            # Absorption at 0
            rt_prev_positive = np.maximum(rt_prev, 0.0)
            
            dW = np.random.normal(0, np.sqrt(dt), size=paths)
            r[t, :] = rt_prev + self.kappa * (self.theta - rt_prev) * dt + self.sigma * np.sqrt(rt_prev_positive) * dW
            
        return r

    def simulate_exact(self, r0: float, T: float, steps: int, paths: int = 1) -> np.ndarray:
        """
        Simulates interest rate paths using exact transition density (Non-central chi-squared).
        """
        dt = T / steps
        r = np.zeros((steps + 1, paths))
        r[0, :] = r0
        
        # transition parameters
        c = 2 * self.kappa / (self.sigma**2 * (1 - np.exp(-self.kappa * dt)))
        d = 4 * self.kappa * self.theta / (self.sigma**2)
        
        for t in range(1, steps + 1):
            rt_prev = r[t-1, :]
            nc = 2 * c * rt_prev * np.exp(-self.kappa * dt)
            # Draw from non-central chi-squared distribution
            # r_t = chi2(df=d, nc=nc) / (2 * c)
            # numpy's random.noncentral_chisquare takes degrees of freedom (df) and noncentrality (nonc)
            # Note: numpy's nonc is exactly lambda_c in standard literature
            r_draw = np.random.noncentral_chisquare(df=d, nonc=nc, size=paths)
            r[t, :] = r_draw / (2 * c)
            
        return r
