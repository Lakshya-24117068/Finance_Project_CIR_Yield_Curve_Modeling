import numpy as np
from typing import Dict
from src.pricing.yield_curve import CIRYieldCurve

class CIRPlusPlusYieldCurve(CIRYieldCurve):
    def __init__(self, pricer, shift_map: Dict[float, float]):
        """
        CIR++ yield curve calculation adjusting base yields by shift function phi.
        """
        super().__init__(pricer)
        self.shift_map = shift_map

    def calculate_yield(self, rt: float, tau: float) -> float:
        y_base = super().calculate_yield(rt, tau)
        # Add deterministic shift
        shift = self.shift_map.get(tau, 0.0)
        return y_base + shift
