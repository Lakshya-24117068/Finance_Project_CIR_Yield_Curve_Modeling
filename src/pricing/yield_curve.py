import numpy as np
from src.pricing.bond_pricing import CIRBondPricer

class CIRYieldCurve:
    def __init__(self, pricer: CIRBondPricer):
        self.pricer = pricer

    def calculate_yield(self, rt: float, tau: float) -> float:
        """Calculates yield for maturity tau based on ZCB pricing coefficients."""
        A, B = self.pricer.get_zcb_price_coeff(tau)
        # Handle zero or negative A safely to avoid issues with log
        A_clean = np.maximum(A, 1e-15)
        y = (B * rt - np.log(A_clean)) / tau
        return y

    def calculate_yield_curve(self, rt: np.ndarray, maturities: np.ndarray) -> np.ndarray:
        """
        Calculates yield curve vectors for each day in short rate array rt.
        Returns a matrix of shape (len(rt), len(maturities))
        """
        num_days = len(rt)
        num_mats = len(maturities)
        yield_matrix = np.zeros((num_days, num_mats))
        
        for j, tau in enumerate(maturities):
            yield_matrix[:, j] = self.calculate_yield(rt, tau)
            
        return yield_matrix
