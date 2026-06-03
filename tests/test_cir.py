import numpy as np
from src.models.cir import CIRModel

def test_cir_parameters():
    model = CIRModel(kappa=0.2, theta=0.03, sigma=0.05)
    assert model.kappa == 0.2
    assert model.theta == 0.03
    assert model.sigma == 0.05
    assert model.verify_feller() == True

def test_cir_simulation():
    model = CIRModel(kappa=0.5, theta=0.02, sigma=0.05)
    r = model.simulate_euler(r0=0.02, T=1.0, steps=252, paths=5)
    assert r.shape == (253, 5)
    # Yields should remain positive
    assert np.all(r >= 0)
