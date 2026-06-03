import pandas as pd
import numpy as np
from src.data.cleaner import DataCleaner

def test_data_cleaning():
    mock_data = pd.DataFrame({
        'Date': ['2026-06-01', '2026-06-02', '2026-06-02', '2026-06-03'],  # Duplicate date
        ' ZC025YR': [0.02, 0.03, 0.03, 0.025],
        ' ZC050YR': [0.022, np.nan, 0.032, 0.027]  # Missing value
    })
    
    # Strip spaces
    mock_data.columns = [c.strip() for c in mock_data.columns]
    
    cleaner = DataCleaner()
    cleaned = cleaner.clean(mock_data)
    
    # Verify duplicates are dropped (should have 3 rows)
    assert len(cleaned) == 3
    # Verify missing value is interpolated (no NaNs left)
    assert cleaned['ZC050YR'].isnull().sum() == 0
