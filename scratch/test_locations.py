from src.ingestion.loader import load_raw_dataset
from src.ingestion.preprocessor import preprocess

raw_df = load_raw_dataset()
clean_df = preprocess(raw_df)

print(clean_df['location'].unique()[:20])
