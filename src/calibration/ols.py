import numpy as np
import pandas as pd
from typing import Tuple
from src.utils.helpers import get_logger

logger = get_logger(__name__)

class OLSCalibrator:
    def __init__(self, dt: float = 1.0/252.0):
        self.dt = dt

    def calibrate(self, short_rates: np.ndarray) -> Tuple[float, float, float]:
        """
        Calibrates CIR using Ordinary Least Squares on Euler-discretized increments.
        dr_t / sqrt(r_t) = kappa*theta*dt / sqrt(r_t) - kappa*sqrt(r_t)*dt + sigma*sqrt(dt)*eps
        """
        dr = np.diff(short_rates)
        rt_prev = short_rates[:-1]
        
        y = dr / np.sqrt(rt_prev)
        x1 = self.dt / np.sqrt(rt_prev)
        x2 = -np.sqrt(rt_prev) * self.dt
        
        X = np.column_stack((x1, x2))
        beta, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)
        
        beta1, beta2 = beta
        kappa = beta2
        theta = beta1 / beta2
        
        residuals_var = np.var(y - X @ beta)
        sigma = np.sqrt(residuals_var / self.dt)
        
        logger.info(f"OLS Calibration complete: kappa={kappa:.6f}, theta={theta:.6f}, sigma={sigma:.6f}")
        return kappa, theta, sigma
