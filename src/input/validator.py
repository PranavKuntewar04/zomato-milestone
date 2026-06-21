from src.input.models import UserPreference

VALID_BUDGETS = {"low", "medium", "high"}

def collect_and_validate() -> UserPreference:
    """Interactively collect and validate user preferences from CLI."""

    print("\n🍽️  Welcome to the Zomato AI Restaurant Recommender!\n")

    location = input("📍 Enter your location (e.g., Delhi, Bangalore): ").strip()
    if not location:
        raise ValueError("Location cannot be empty.")

    budget = input("💰 Enter budget [low / medium / high]: ").strip().lower()
    if budget not in VALID_BUDGETS:
        raise ValueError(f"Budget must be one of: {', '.join(VALID_BUDGETS)}")

    cuisine = input("🍜 Enter preferred cuisine (e.g., North Indian, Chinese): ").strip()
    if not cuisine:
        raise ValueError("Cuisine cannot be empty.")

    rating_str = input("⭐ Minimum rating (1.0 – 5.0, e.g., 3.5): ").strip()
    try:
        min_rating = float(rating_str)
        if not (1.0 <= min_rating <= 5.0):
            raise ValueError()
    except ValueError:
        raise ValueError("Rating must be a number between 1.0 and 5.0.")

    additional_prefs = input(
        "✨ Any additional preferences? (e.g., family-friendly, rooftop) [Press Enter to skip]: "
    ).strip()

    return UserPreference(
        location=location.lower(),
        budget=budget,
        cuisine=cuisine.lower(),
        min_rating=min_rating,
        additional_prefs=additional_prefs,
    )
