import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from src.utils.config import FIGURES_DIR
from src.visualization.plots import plot_actual_vs_predicted, plot_yield_curve_reconstruction

def generate_reports_figures(test_df: pd.DataFrame, predicted_curves: dict) -> None:
    """
    Generates and saves research-quality figures to reports/figures/ folder.
    """
    dates = pd.to_datetime(test_df['Date'])
    
    # Save a sample actual vs predicted curve for ZC050YR and ZC200YR
    for tenor in ['ZC050YR', 'ZC200YR']:
        if tenor in test_df.columns and tenor in predicted_curves:
            y_act = test_df[tenor].values
            y_pred = predicted_curves[tenor]
            save_path = os.path.join(FIGURES_DIR, f"{tenor}_reconstruction_plot.png")
            plot_actual_vs_predicted(dates, y_act, y_pred, f"Out-of-Sample {tenor} Reconstruction", save_path)
            
    # Save cross-sectional yield curve plot
    first_row = test_df.iloc[0]
    tau = [0.25, 0.50, 0.75, 1.00, 2.00]
    y_act = first_row[['ZC025YR', 'ZC050YR', 'ZC075YR', 'ZC100YR', 'ZC200YR']].values
    
    # Reconstruct prediction curve
    rt = y_act[0]
    # Simple model prediction placeholder to map to function call (requires pricer/yield_curve in real script)
    # We will generate this in the backtester
