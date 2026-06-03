import numpy as np
from src.models.cir import CIRModel

class TwoFactorCIRModel:
    def __init__(self, cir1: CIRModel, cir2: CIRModel):
        """
        Two-Factor CIR model: r_t = x_1,t + x_2,t
        where x_1 and x_2 are independent CIR processes.
        """
        self.cir1 = cir1
        self.cir2 = cir2

    def decompose_short_rate(self, rt: np.ndarray, ema_span: int = 20) -> tuple:
        """
        Decomposes the short rate rt into long-term factor x2 (exponential moving average)
        and short-term factor x1 (residuals).
        """
        # Convert to pandas Series to compute EMA
        s = pd = ema_series = np.array(rt)
        ema = np.zeros_like(s)
        
        # Simple EMA filter
        alpha = 2.0 / (ema_span + 1.0)
        ema[0] = s[0]
        for i in range(1, len(s)):
            ema[i] = alpha * s[i] + (1 - alpha) * ema[i-1]
            
        # x2 = long term trend
        x2 = ema
        # x1 = deviation, floored at 0 to guarantee positivity
        x1 = np.maximum(s - x2, 1e-6)
        
        return x1, x2
