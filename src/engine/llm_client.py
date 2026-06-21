import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds (doubles each retry)


def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_actual_groq_api_key_here":
        raise EnvironmentError(
            "GROQ_API_KEY not found or is invalid. Please set a valid key in your .env file."
        )
    return Groq(api_key=api_key)


def call_groq(system_prompt: str, user_prompt: str) -> str:
    """
    Send prompt to Groq API and return the raw text response.
    Retries up to MAX_RETRIES times on failure.
    """
    client = get_groq_client()
    model = os.getenv("GROQ_MODEL", "llama3-8b-8192")

    delay = RETRY_DELAY
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=2048,
            )
            return response.choices[0].message.content

        except Exception as e:
            if attempt == MAX_RETRIES:
                raise RuntimeError(
                    f"Groq API call failed after {MAX_RETRIES} attempts: {e}"
                )
            print(f"⚠️  Groq API error (attempt {attempt}/{MAX_RETRIES}): {e}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
