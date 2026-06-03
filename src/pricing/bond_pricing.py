import numpy as np
from typing import Tuple

class CIRBondPricer:
    def __init__(self, kappa: float, theta: float, sigma: float):
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma

    def get_zcb_price_coeff(self, tau: float) -> Tuple[float, float]:
        """
        Returns the analytical pricing coefficients A(t, T) and B(t, T) under CIR.
        """
        h = np.sqrt(self.kappa**2 + 2 * self.sigma**2)
        exp_ht = np.exp(h * tau)
        
        denominator = (h + self.kappa) * (exp_ht - 1) + 2 * h
        
        # A(t, T)
        numerator_A = 2 * h * np.exp((h + self.kappa) * tau / 2)
        exponent = (2 * self.kappa * self.theta) / (self.sigma**2)
        A = (numerator_A / denominator) ** exponent
        
        # B(t, T)
        numerator_B = 2 * (exp_ht - 1)
        B = numerator_B / denominator
        
        return A, B

    def price_zero_coupon_bond(self, rt: float, tau: float) -> float:
        """Prices a zero coupon bond maturing at T with time to maturity tau."""
        A, B = self.get_zcb_price_coeff(tau)
        price = A * np.exp(-B * rt)
        return price
