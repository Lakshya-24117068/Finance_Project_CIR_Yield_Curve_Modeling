import numpy as np
from scipy.optimize import minimize
from typing import Tuple
from src.utils.helpers import get_logger

logger = get_logger(__name__)

class GMMCalibrator:
    def __init__(self, dt: float = 1.0/252.0):
        self.dt = dt

    def calibrate(self, short_rates: np.ndarray) -> Tuple[float, float, float]:
        """
        Calibrates CIR using Generalized Method of Moments.
        Based on conditional mean and conditional variance moments:
        e1 = r_t - E[r_t | r_{t-1}]
        e2 = e1^2 - Var(r_t | r_{t-1})
        Moments: E[e1] = 0, E[e1 * r_{t-1}] = 0, E[e2] = 0, E[e2 * r_{t-1}] = 0
        """
        r_t = short_rates[1:]
        r_t_prev = short_rates[:-1]
        
        def gmm_objective(params):
            kappa, theta, sigma = params
            if kappa <= 0 or theta <= 0 or sigma <= 0:
                return 1e10
                
            exp_kd = np.exp(-kappa * self.dt)
            cond_mean = r_t_prev * exp_kd + theta * (1 - exp_kd)
            cond_var = r_t_prev * (sigma**2 / kappa) * (exp_kd - exp_kd**2) + theta * (sigma**2 / (2 * kappa)) * (1 - exp_kd)**2
            
            e1 = r_t - cond_mean
            e2 = e1**2 - cond_var
            
            # Moment equations
            m1 = e1
            m2 = e1 * r_t_prev
            m3 = e2
            m4 = e2 * r_t_prev
            
            # Average moments
            g = np.array([np.mean(m1), np.mean(m2), np.mean(m3), np.mean(m4)])
            
            # Identity weighting matrix initially
            return g.T @ g

        initial_guess = [0.1, 0.02, 0.05]
        bounds = ((1e-5, 10.0), (1e-5, 1.0), (1e-5, 1.0))
        
        res = minimize(gmm_objective, initial_guess, bounds=bounds, method='L-BFGS-B')
        
        if res.success:
            kappa, theta, sigma = res.x
            logger.info(f"GMM Calibration complete: kappa={kappa:.6f}, theta={theta:.6f}, sigma={sigma:.6f}")
            return kappa, theta, sigma
        else:
            raise RuntimeError(f"GMM optimization failed: {res.message}")
