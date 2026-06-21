import pandas as pd
from src.input.models import UserPreference

MAX_RESULTS = 15  # Maximum candidates sent to LLM

def filter_restaurants(df: pd.DataFrame, prefs: UserPreference) -> pd.DataFrame:
    """Apply sequential AND-filters based on user preferences."""

    filtered = df.copy()

    # Filter 1: Location (partial match)
    if prefs.location and prefs.location.lower() != "any":
        filtered = filtered[filtered["location"].str.contains(prefs.location, case=False, na=False)]

    # Filter 2: Cuisine (partial match)
    if prefs.cuisine and prefs.cuisine.lower() != "any":
        filtered = filtered[filtered["cuisines"].str.contains(prefs.cuisine, case=False, na=False)]

    # Filter 3: Budget tier (exact match)
    if prefs.budget and prefs.budget.lower() != "any":
        filtered = filtered[filtered["budget_tier"] == prefs.budget]

    # Filter 4: Minimum rating
    if prefs.min_rating and prefs.min_rating > 1.0:
        filtered = filtered[filtered["rating"] >= prefs.min_rating]

    # Sort by rating descending; take top-N
    filtered = filtered.sort_values("rating", ascending=False).head(MAX_RESULTS)

    return filtered.reset_index(drop=True)


def filter_with_fallback(df: pd.DataFrame, prefs: UserPreference) -> tuple[pd.DataFrame, list[str]]:
    """
    Try strict filtering first. If < 3 results, progressively relax lower-priority filters.
    Returns: (filtered_df, list of relaxed filter names)
    """
    relaxed = []
    result = filter_restaurants(df, prefs)

    if len(result) < 3:
        # Relax cuisine filter
        relaxed.append("cuisine")
        relaxed_prefs = UserPreference(
            location=prefs.location,
            budget=prefs.budget,
            cuisine="",          # Remove cuisine filter
            min_rating=prefs.min_rating,
            additional_prefs=prefs.additional_prefs,
        )
        result = filter_restaurants(df, relaxed_prefs)

    if len(result) < 3:
        # Relax budget filter
        relaxed.append("budget")
        filtered = df[df["location"].str.contains(prefs.location, case=False, na=False)]
        filtered = filtered[filtered["rating"] >= prefs.min_rating]
        result = filtered.sort_values("rating", ascending=False).head(MAX_RESULTS).reset_index(drop=True)

    return result, relaxed
