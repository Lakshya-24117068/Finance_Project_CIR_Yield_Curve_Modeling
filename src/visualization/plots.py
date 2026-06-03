import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List, Dict

def plot_actual_vs_predicted(dates: pd.Series, y_act: np.ndarray, y_pred: np.ndarray, title: str, save_path: str = None) -> None:
    """Plots historical actual yields vs predictions."""
    plt.figure(figsize=(10, 5))
    plt.plot(dates, y_act * 100, label="Actual", color="#1f77b4", linewidth=1.5)
    plt.plot(dates, y_pred * 100, label="Predicted (CIR)", color="#ff7f0e", linestyle="--", linewidth=1.5)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Yield (%)")
    plt.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        plt.close()
    else:
        plt.show()

def plot_yield_curve_reconstruction(tau: List[float], y_act: np.ndarray, y_pred: np.ndarray, date_str: str, save_path: str = None) -> None:
    """Plots cross-sectional yield curves (actual vs predicted) for a specific date."""
    plt.figure(figsize=(9, 5))
    plt.plot(tau, y_act * 100, 'o-', label="Actual Market Curve", color="#1f77b4", linewidth=2)
    plt.plot(tau, y_pred * 100, 's--', label="Reconstructed CIR Curve", color="#ff7f0e", linewidth=2)
    plt.title(f"Yield Curve Reconstruction - {date_str}")
    plt.xlabel("Maturity (Years)")
    plt.ylabel("Yield (%)")
    plt.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        plt.close()
    else:
        plt.show()
