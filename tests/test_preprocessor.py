import pandas as pd
from src.ingestion.preprocessor import preprocess, assign_budget_tier

def test_budget_tier_assignment():
    assert assign_budget_tier(300)  == "low"
    assert assign_budget_tier(800)  == "medium"
    assert assign_budget_tier(2000) == "high"

def test_preprocess_drops_nulls():
    raw = pd.DataFrame({
        "name": ["A", None],
        "location": ["delhi", "mumbai"],
        "cuisines": ["north indian", "chinese"],
        "approx_cost(for two people)": ["500", "800"],
        "rate": ["4.1/5", "3.8/5"],
    })
    result = preprocess(raw)
    assert len(result) == 1
    assert result.iloc[0]["name"] == "A"
