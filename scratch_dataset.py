from src.ingestion.loader import load_raw_dataset

try:
    df = load_raw_dataset()
    print("Columns:", df.columns.tolist())
    print("\nHead:")
    print(df.head())
except Exception as e:
    print("Error:", e)
