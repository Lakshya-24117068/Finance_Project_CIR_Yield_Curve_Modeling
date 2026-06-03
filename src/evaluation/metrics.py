import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

def get_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Computes regression evaluation metrics: R2, RMSE, MAE, MAPE.
    """
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    
    # MAPE (exclude zeros to avoid zero division)
    mask = y_true != 0.0
    mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    
    return {
        "R2": r2,
        "RMSE": rmse,
        "MAE": mae,
        "MAPE": mape
    }
