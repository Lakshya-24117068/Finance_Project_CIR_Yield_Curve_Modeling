import pandas as pd
import numpy as np
from typing import List
from src.utils.helpers import get_logger

logger = get_logger(__name__)

class DataCleaner:
    def __init__(self, z_score_threshold: float = 3.5, iqr_multiplier: float = 2.5):
        self.z_score_threshold = z_score_threshold
        self.iqr_multiplier = iqr_multiplier

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Performs full data cleaning sequence:
        1. Duplicate removal
        2. Column stripping
        3. Missing value interpolation (or forward fill)
        4. Outlier removal & smoothing
        """
        df_cleaned = df.copy()
        
        # 1. Stripping string columns
        for col in df_cleaned.columns:
            if df_cleaned[col].dtype == object:
                df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
                
        # 2. Remove duplicates
        initial_len = len(df_cleaned)
        df_cleaned.drop_duplicates(subset=['Date'], inplace=True)
        final_len = len(df_cleaned)
        if initial_len != final_len:
            logger.info(f"Removed {initial_len - final_len} duplicate date records.")
            
        # Sort by date
        df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'])
        df_cleaned.sort_values(by='Date', inplace=True)
        df_cleaned.reset_index(drop=True, inplace=True)
        
        # 3. Handle missing values
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        null_count = df_cleaned[numeric_cols].isnull().sum().sum()
        if null_count > 0:
            logger.info(f"Found {null_count} missing values. Performing linear interpolation & forward-fill.")
            df_cleaned[numeric_cols] = df_cleaned[numeric_cols].interpolate(method='linear')
            df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(method='ffill').fillna(method='bfill')
            
        # 4. Outlier removal and cleaning
        df_cleaned = self.clean_outliers(df_cleaned, list(numeric_cols))
        
        return df_cleaned

    def clean_outliers(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Detects outliers on daily differences using a rolling median and IQR method.
        Replaces outliers with the rolling median + bounds.
        """
        df_cleaned = df.copy()
        
        for col in columns:
            yields = df_cleaned[col].values
            diffs = np.diff(yields)
            
            # Simple Z-score check on differences
            mean_diff = np.mean(diffs)
            std_diff = np.std(diffs)
            if std_diff == 0:
                continue
                
            z_scores = np.abs((diffs - mean_diff) / std_diff)
            outliers_idx = np.where(z_scores > self.z_score_threshold)[0]
            
            if len(outliers_idx) > 0:
                logger.info(f"Outlier detection in {col}: Found {len(outliers_idx)} daily jump outliers. Smoothing.")
                for idx in outliers_idx:
                    # Smoothing outlier step by taking average of adjacent days
                    # idx in diffs corresponds to idx+1 in yields
                    y_idx = idx + 1
                    if 0 < y_idx < len(yields) - 1:
                        yields[y_idx] = (yields[y_idx-1] + yields[y_idx+1]) / 2.0
                    elif y_idx == len(yields) - 1:
                        yields[y_idx] = yields[y_idx-1]
                df_cleaned[col] = yields
                
        return df_cleaned
