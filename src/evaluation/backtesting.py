import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
from src.pricing.bond_pricing import CIRBondPricer
from src.pricing.yield_curve import CIRYieldCurve
from src.evaluation.metrics import get_regression_metrics
from src.utils.helpers import get_logger

logger = get_logger(__name__)

class YieldCurveBacktester:
    def __init__(self, pricer: CIRBondPricer):
        self.curve_model = CIRYieldCurve(pricer)

    def backtest(self, test_df: pd.DataFrame, maturities: Dict[str, float]) -> Tuple[float, Dict[str, dict]]:
        """
        Reconstructs the yield curve from short rate (3M) and returns accuracy metrics.
        """
        rt = test_df['ZC025YR'].values
        results = {}
        
        actual_list = []
        pred_list = []
        
        logger.info("Starting out-of-sample yield curve backtest...")
        
        for col, tau in maturities.items():
            y_act = test_df[col].values
            y_pred = self.curve_model.calculate_yield(rt, tau)
            
            metrics = get_regression_metrics(y_act, y_pred)
            results[col] = metrics
            
            actual_list.append(y_act)
            pred_list.append(y_pred)
            
        actual_flat = np.concatenate(actual_list)
        pred_flat = np.concatenate(pred_list)
        
        overall_metrics = get_regression_metrics(actual_flat, pred_flat)
        logger.info(f"Backtest complete. Overall R2 score: {overall_metrics['R2']:.4f}")
        
        return overall_metrics['R2'], results
