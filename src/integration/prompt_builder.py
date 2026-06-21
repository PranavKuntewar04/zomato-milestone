from src.input.models import UserPreference

SYSTEM_PROMPT = """You are an expert restaurant recommendation assistant.
Your task is to rank and explain restaurant suggestions based on a user's stated preferences.
Be concise, helpful, and personalized in your responses.
Always output results in the exact structured format specified — do not deviate from it."""


def build_user_prompt(formatted_restaurants: str, prefs: UserPreference) -> str:
    """Assemble the final user prompt for the Groq LLM."""

    additional = prefs.additional_prefs if prefs.additional_prefs else "None"

    return f"""The user is looking for a restaurant with the following preferences:
- Location:               {prefs.location.title()}
- Budget:                 {prefs.budget.capitalize()}
- Preferred Cuisine:      {prefs.cuisine.title()}
- Minimum Rating:         {prefs.min_rating}
- Additional Preferences: {additional}

Based on these preferences, here are the candidate restaurants retrieved from our database:

{formatted_restaurants}

Please:
1. Rank these restaurants from BEST to LEAST suitable for this user.
2. For each restaurant, provide a 2-3 sentence explanation of WHY it is a good (or less ideal) match.
3. Provide a brief 1-2 sentence overall summary of the top recommendation.

Format your response EXACTLY as follows (do not add any extra text outside this format):
---
Rank 1: [Restaurant Name]
Explanation: [Your explanation here]

Rank 2: [Restaurant Name]
Explanation: [Your explanation here]

(continue for all restaurants)
---
Overall Summary: [Brief summary of top pick]
"""
