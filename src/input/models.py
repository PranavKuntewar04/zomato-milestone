from dataclasses import dataclass, field

@dataclass
class UserPreference:
    location: str = "any"
    budget: str = "any"            # "low" | "medium" | "high" | "any"
    cuisine: str = "any"
    min_rating: float = 1.0        # e.g., 3.5
    additional_prefs: str = field(default="")  # Optional free-form text
