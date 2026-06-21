from src.input.models import UserPreference

def test_user_preference_creation():
    pref = UserPreference(
        location="delhi",
        budget="medium",
        cuisine="north indian",
        min_rating=4.0,
        additional_prefs="family-friendly"
    )
    assert pref.location == "delhi"
    assert pref.budget == "medium"
    assert pref.min_rating == 4.0
