from src.integration.prompt_builder import build_user_prompt, SYSTEM_PROMPT
from src.input.models import UserPreference

def test_prompt_contains_preferences():
    prefs = UserPreference(location="delhi", budget="medium", cuisine="north indian", min_rating=4.0)
    prompt = build_user_prompt("Restaurant 1:\n  Name: Spice Garden\n", prefs)
    assert "Delhi" in prompt
    assert "Medium" in prompt
    assert "4.0" in prompt
    assert "Spice Garden" in prompt

def test_system_prompt_is_non_empty():
    assert len(SYSTEM_PROMPT) > 0
