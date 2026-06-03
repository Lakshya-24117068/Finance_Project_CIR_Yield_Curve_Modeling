import numpy as np
from typing import Tuple

def calculate_confidence_intervals(params: np.ndarray, hessian_inv: np.ndarray, alpha: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
    """
    Estimates parameters confidence intervals using the diagonal of the inverse Hessian matrix.
    """
    std_errors = np.sqrt(np.diag(hessian_inv))
    margin_error = 1.96 * std_errors  # 95% Confidence Interval
    
    ci_lower = params - margin_error
    ci_upper = params + margin_error
    
    return ci_lower, ci_upper
