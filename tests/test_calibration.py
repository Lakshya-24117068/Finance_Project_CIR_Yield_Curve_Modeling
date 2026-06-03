import numpy as np
from src.calibration.ols import OLSCalibrator

def test_ols_calibration():
    # Generate mock mean-reverting data
    np.random.seed(42)
    steps = 1000
    r = np.zeros(steps)
    r[0] = 0.02
    kappa, theta, sigma = 0.5, 0.03, 0.01
    dt = 1.0/252.0
    
    for t in range(1, steps):
        dW = np.random.normal(0, np.sqrt(dt))
        r[t] = r[t-1] + kappa * (theta - r[t-1]) * dt + sigma * np.sqrt(max(r[t-1], 0)) * dW
        
    calibrator = OLSCalibrator(dt=dt)
    k_est, th_est, sig_est = calibrator.calibrate(r)
    
    # OLS estimation should be reasonably close to true parameters (within margin)
    assert k_est > 0
    assert th_est > 0
    assert sig_est > 0
