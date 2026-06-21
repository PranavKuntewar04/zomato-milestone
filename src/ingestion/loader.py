import os
import pandas as pd
from datasets import load_dataset

CLEAN_PARQUET_FILE = "data/clean_dataset.parquet"

def load_raw_dataset() -> pd.DataFrame:
    """Load the pre-cleaned Zomato dataset from local parquet."""
    if os.path.exists(CLEAN_PARQUET_FILE):
        return pd.read_parquet(CLEAN_PARQUET_FILE)
    
    raise FileNotFoundError(f"Cleaned dataset not found at {CLEAN_PARQUET_FILE}")
