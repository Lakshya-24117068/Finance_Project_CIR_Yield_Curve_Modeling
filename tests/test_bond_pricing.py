import numpy as np
from src.pricing.bond_pricing import CIRBondPricer
from src.pricing.yield_curve import CIRYieldCurve

def test_bond_pricing_limits():
    # If time to maturity tau is 0, ZCB price should be 1.0, and A=1.0, B=0.0
    pricer = CIRBondPricer(kappa=0.1, theta=0.02, sigma=0.01)
    A, B = pricer.get_zcb_price_coeff(tau=0.0)
    assert np.isclose(A, 1.0)
    assert np.isclose(B, 0.0)
    
    price = pricer.price_zero_coupon_bond(rt=0.03, tau=0.0)
    assert np.isclose(price, 1.0)

def test_yield_curve_calculation():
    pricer = CIRBondPricer(kappa=0.1, theta=0.02, sigma=0.01)
    curve = CIRYieldCurve(pricer)
    # Yield at very short maturity should be close to short rate rt
    y = curve.calculate_yield(rt=0.03, tau=1e-5)
    assert np.isclose(y, 0.03, rtol=1e-2)
