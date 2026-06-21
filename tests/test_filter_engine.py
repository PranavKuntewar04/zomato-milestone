import pandas as pd
from src.integration.filter_engine import filter_restaurants
from src.input.models import UserPreference

def make_test_df():
    return pd.DataFrame({
        "name": ["Spice Garden", "Pizza House", "Curry Point"],
        "location": ["delhi, connaught place", "mumbai, bandra", "delhi, lajpat nagar"],
        "cuisines": ["north indian", "italian", "north indian"],
        "cost_for_two": [600.0, 900.0, 400.0],
        "rating": [4.3, 4.1, 3.9],
        "budget_tier": ["medium", "medium", "low"],
    })

def test_filter_by_location():
    df = make_test_df()
    prefs = UserPreference(location="delhi", budget="medium", cuisine="north indian", min_rating=4.0)
    result = filter_restaurants(df, prefs)
    assert len(result) == 1
    assert result.iloc[0]["name"] == "Spice Garden"

def test_filter_returns_empty_when_no_match():
    df = make_test_df()
    prefs = UserPreference(location="kolkata", budget="low", cuisine="chinese", min_rating=4.5)
    result = filter_restaurants(df, prefs)
    assert result.empty
