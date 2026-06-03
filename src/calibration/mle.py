import numpy as np
from scipy.optimize import minimize
from scipy.stats import ncx2
from typing import Tuple
from src.utils.helpers import get_logger

logger = get_logger(__name__)

class MLECalibrator:
    def __init__(self, dt: float = 1.0/252.0):
        self.dt = dt

    def calibrate(self, short_rates: np.ndarray) -> Tuple[float, float, float]:
        """
        Calibrates CIR using exact Maximum Likelihood Estimation.
        Uses transition density based on non-central chi-squared distribution:
        f(r_t | r_{t-1}) = 2 * c * ncx2.pdf(2 * c * r_t, df=d, nc=nc)
        """
        rt = short_rates
        r_t = rt[1:]
        r_t_prev = rt[:-1]
        
        def log_likelihood(params):
            kappa, theta, sigma = params
            if kappa <= 0 or theta <= 0 or sigma <= 0:
                return 1e10
                
            c = 2 * kappa / (sigma**2 * (1 - np.exp(-kappa * self.dt)))
            d = 4 * kappa * theta / (sigma**2)
            
            # Non-centrality parameter
            nc = 2 * c * r_t_prev * np.exp(-kappa * self.dt)
            # Transition values scaled
            x_vals = 2 * c * r_t
            
            # Compute PDF safely to avoid log of zero or negative density values
            pdf_vals = 2 * c * ncx2.pdf(x_vals, df=d, nc=nc)
            
            # Clean zero or NaN values
            pdf_vals = np.where(pdf_vals <= 1e-10, 1e-10, pdf_vals)
            pdf_vals = np.where(np.isnan(pdf_vals), 1e-10, pdf_vals)
            
            return -np.sum(np.log(pdf_vals))

        # Initial guess from stable parameters
        initial_guess = [0.1, 0.02, 0.05]
        bounds = ((1e-5, 10.0), (1e-5, 1.0), (1e-5, 1.0))
        
        res = minimize(log_likelihood, initial_guess, bounds=bounds, method='L-BFGS-B')
        
        if res.success:
            kappa, theta, sigma = res.x
            logger.info(f"MLE Calibration complete: kappa={kappa:.6f}, theta={theta:.6f}, sigma={sigma:.6f}")
            return kappa, theta, sigma
        else:
            raise RuntimeError(f"MLE optimization failed: {res.message}")
