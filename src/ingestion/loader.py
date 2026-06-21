import os
import pandas as pd
from datasets import load_dataset

DATASET_NAME = "ManikaSaini/zomato-restaurant-recommendation"
PARQUET_FILE = "data/zomato_dataset.parquet"

def load_raw_dataset() -> pd.DataFrame:
    """Load the Zomato dataset from local parquet or Hugging Face Hub."""
    if os.path.exists(PARQUET_FILE):
        return pd.read_parquet(PARQUET_FILE)
    
    # Fallback to downloading if parquet doesn't exist
    dataset = load_dataset(DATASET_NAME, split="train")
    return dataset.to_pandas()
