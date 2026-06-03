import os
import pandas as pd
from typing import Tuple
from src.utils.config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.utils.helpers import get_logger

logger = get_logger(__name__)

class DataLoader:
    def __init__(self, raw_dir: str = RAW_DATA_DIR, processed_dir: str = PROCESSED_DATA_DIR):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir

    def load_raw_data(self, filename: str) -> pd.DataFrame:
        """Loads CSV file from raw directory, cleaning whitespaces in columns."""
        path = os.path.join(self.raw_dir, filename)
        logger.info(f"Loading raw data from {path}")
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        # skipinitialspace=True handles spaces in CSV header
        df = pd.read_csv(path, skipinitialspace=True)
        return df

    def load_processed_data(self, filename: str) -> pd.DataFrame:
        """Loads preprocessed CSV file from processed directory."""
        path = os.path.join(self.processed_dir, filename)
        logger.info(f"Loading processed data from {path}")
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        df = pd.read_csv(path)
        return df

    def save_processed_data(self, df: pd.DataFrame, filename: str) -> None:
        """Saves cleaned DataFrame to processed directory."""
        path = os.path.join(self.processed_dir, filename)
        logger.info(f"Saving processed data to {path}")
        df.to_csv(path, index=False)
