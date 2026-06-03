import numpy as np
from typing import Dict, Union, List
from src.models.cir import CIRModel

class CIRPlusPlusModel:
    def __init__(self, cir_model: CIRModel, shift_map: Dict[float, float] = None):
        """
        CIR++ model: r_t = x_t + phi(t)
        where x_t is standard CIR and phi(t) is a deterministic function of maturity.
        """
        self.cir = cir_model
        self.shift_map = shift_map if shift_map is not None else {}

    def get_shift(self, tau: float) -> float:
        """Returns the deterministic shift value for maturity tau (uses nearest if not exact)."""
        if not self.shift_map:
            return 0.0
        if tau in self.shift_map:
            return self.shift_map[tau]
            
        # Match nearest maturity
        keys = list(self.shift_map.keys())
        nearest_key = min(keys, key=lambda x: abs(x - tau))
        return self.shift_map[nearest_key]
