import pandas as pd

BUDGET_TIERS = {
    "low":    (0,    500),
    "medium": (501,  1200),
    "high":   (1201, float("inf")),
}

def assign_budget_tier(cost: float) -> str:
    for tier, (low, high) in BUDGET_TIERS.items():
        if low <= cost <= high:
            return tier
    return "high"

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize the raw Zomato DataFrame."""

    # 1. Rename columns to standard names
    df = df.rename(columns={
        "name": "name",
        "location": "location",
        "cuisines": "cuisines",
        "approx_cost(for two people)": "cost_for_two",
        "rate": "rating",
    })

    # 2. Keep only required columns
    required_cols = ["name", "location", "cuisines", "cost_for_two", "rating"]
    df = df[[c for c in required_cols if c in df.columns]].copy()

    # 3. Drop rows with missing critical fields
    df.dropna(subset=["name", "location", "cuisines", "cost_for_two", "rating"], inplace=True)

    # 3.5 Remove duplicates
    df.drop_duplicates(inplace=True)

    # 4. Clean cost_for_two — remove commas, cast to float
    df["cost_for_two"] = (
        df["cost_for_two"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df = df[df["cost_for_two"].str.match(r"^\d+(\.\d+)?$")]
    df["cost_for_two"] = df["cost_for_two"].astype(float)

    # 5. Clean rating — handle "NEW", "-", etc.
    df["rating"] = (
        df["rating"]
        .astype(str)
        .str.extract(r"(\d+\.\d+|\d+)")[0]
        .astype(float)
    )
    df = df[(df["rating"] >= 1.0) & (df["rating"] <= 5.0)]

    # 6. Normalize text fields
    df["location"] = df["location"].str.strip().str.lower()
    df["cuisines"] = df["cuisines"].str.strip().str.lower()
    df["name"] = df["name"].str.strip()

    # 7. Add budget tier
    df["budget_tier"] = df["cost_for_two"].apply(assign_budget_tier)

    # 8. Reset index
    df.reset_index(drop=True, inplace=True)

    return df
