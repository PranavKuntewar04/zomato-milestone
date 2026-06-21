import pandas as pd

def format_restaurants_for_prompt(df: pd.DataFrame) -> str:
    """Convert filtered DataFrame rows into a structured text block for LLM."""

    if df.empty:
        return "No restaurants found matching the given criteria."

    lines = []
    for i, row in df.iterrows():
        lines.append(f"Restaurant {i + 1}:")
        lines.append(f"  Name:           {row['name']}")
        lines.append(f"  Cuisine:        {row['cuisines'].title()}")
        lines.append(f"  Location:       {row['location'].title()}")
        lines.append(f"  Rating:         {row['rating']} / 5.0")
        lines.append(f"  Cost (for 2):   ₹{int(row['cost_for_two'])} ({row['budget_tier'].capitalize()} budget)")
        lines.append("")  # Blank line between restaurants

    return "\n".join(lines)
