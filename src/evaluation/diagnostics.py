import numpy as np
from scipy import stats

def compute_residuals(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    return y_true - y_pred

def run_normality_test(residuals: np.ndarray) -> Tuple[float, float]:
    """Jarque-Bera normality test on residuals. Returns stat and p-value."""
    jb_stat, p_val = stats.jarque_bera(residuals)
    return jb_stat, p_val

def compute_acf(residuals: np.ndarray, lags: int = 10) -> np.ndarray:
    """Computes autocorrelation of residuals up to specified lag."""
    acf = np.zeros(lags + 1)
    acf[0] = 1.0
    mean = np.mean(residuals)
    var = np.var(residuals)
    if var == 0:
        return acf
    
    n = len(residuals)
    for lag in range(1, lags + 1):
        cov = np.sum((residuals[:-lag] - mean) * (residuals[lag:] - mean)) / n
        acf[lag] = cov / var
    return acf
