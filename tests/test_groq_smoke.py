from src.engine.llm_client import call_groq
from src.integration.prompt_builder import SYSTEM_PROMPT

user_prompt = """The user wants a North Indian restaurant in Delhi with a medium budget and minimum rating 4.0.

Restaurant 1:
  Name: Spice Garden
  Cuisine: North Indian
  Rating: 4.3 / 5.0
  Cost: ₹800 (Medium budget)

Please rank and explain.

---
Rank 1: [Name]
Explanation: [text]
---
Overall Summary: [text]
"""

try:
    response = call_groq(SYSTEM_PROMPT, user_prompt)
    print("GROQ RESPONSE:\n")
    print(response)
except Exception as e:
    print("ERROR DURING SMOKE TEST:", e)
