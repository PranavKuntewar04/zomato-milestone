import os
import pandas as pd
from datasets import load_dataset

DATASET_NAME = "ManikaSaini/zomato-restaurant-recommendation"
DATA_DIR = "data"
PARQUET_FILE = os.path.join(DATA_DIR, "zomato_dataset.parquet")

def download_and_save():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Downloading dataset from Hugging Face...")
    dataset = load_dataset(DATASET_NAME, split="train")
    df = dataset.to_pandas()
    df.to_parquet(PARQUET_FILE, index=False)
    print(f"Successfully saved to {PARQUET_FILE}")

if __name__ == "__main__":
    download_and_save()
