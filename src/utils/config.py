import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")

# Make sure reports folders exist
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(os.path.join(REPORTS_DIR, "tables"), exist_ok=True)
os.makedirs(os.path.join(REPORTS_DIR, "model_results"), exist_ok=True)
