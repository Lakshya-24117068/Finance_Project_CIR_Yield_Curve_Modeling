import pandas as pd
import numpy as np
from typing import List, Dict, Any
from src.utils.helpers import get_logger

logger = get_logger(__name__)

class DataValidator:
    def __init__(self, min_yield: float = 0.0, max_yield: float = 0.20):
        self.min_yield = min_yield
        self.max_yield = max_yield

    def validate(self, df: pd.DataFrame, expected_columns: List[str]) -> Dict[str, Any]:
        """
        Runs verification checks on the DataFrame:
        - Checks column presence
        - Checks non-negativity of yields (for Feller / square root stability)
        - Checks for NaN presence
        - Returns a diagnostic dictionary
        """
        diagnostics = {
            "has_expected_columns": True,
            "missing_columns": [],
            "nan_count": 0,
            "has_negative_yields": False,
            "negative_yields_count": 0,
            "has_unusual_yields": False,
            "unusual_yields_count": 0,
            "valid": True
        }
        
        # Check column presence
        for col in expected_columns:
            if col not in df.columns:
                diagnostics["has_expected_columns"] = False
                diagnostics["missing_columns"].append(col)
                diagnostics["valid"] = False
                
        if not diagnostics["has_expected_columns"]:
            logger.warning(f"Validation FAILED: Missing columns {diagnostics['missing_columns']}")
            return diagnostics

        # Check NaNs
        nan_sum = df[expected_columns].isnull().sum().sum()
        diagnostics["nan_count"] = int(nan_sum)
        if nan_sum > 0:
            diagnostics["valid"] = False
            logger.warning(f"Validation FAILED: Found {nan_sum} NaNs.")

        # Check yield bounds
        numeric_cols = [c for c in expected_columns if c != 'Date']
        yields_data = df[numeric_cols].values
        
        negatives = np.sum(yields_data < self.min_yield)
        diagnostics["negative_yields_count"] = int(negatives)
        if negatives > 0:
            diagnostics["has_negative_yields"] = True
            diagnostics["valid"] = False
            logger.warning(f"Validation FAILED: Found {negatives} negative yield values.")

        unusuals = np.sum(yields_data > self.max_yield)
        diagnostics["unusual_yields_count"] = int(unusuals)
        if unusuals > 0:
            diagnostics["has_unusual_yields"] = True
            logger.warning(f"Validation WARNING: Found {unusuals} yield values greater than {self.max_yield * 100}%.")

        return diagnostics
