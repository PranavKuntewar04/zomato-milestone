import pandas as pd
from src.ingestion.loader import load_raw_dataset
from src.ingestion.preprocessor import preprocess

print("Loading raw dataset...")
raw_df = load_raw_dataset()
print("Preprocessing dataset...")
clean_df = preprocess(raw_df)

print(f"Cleaned dataset has {len(clean_df)} rows and {len(clean_df.columns)} columns.")
clean_df.to_parquet("data/clean_dataset.parquet")
print("Saved to data/clean_dataset.parquet")
