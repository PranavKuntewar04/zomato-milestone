from src.engine.response_parser import parse_llm_response

SAMPLE_RESPONSE = """---
Rank 1: Spice Garden
Explanation: Spice Garden is an excellent match for your preferences. It serves authentic North Indian cuisine in Delhi and is well within the medium budget. The high rating of 4.3 confirms consistently great food and service.

Rank 2: Curry Point
Explanation: Curry Point offers good value North Indian food in Delhi. While the rating is slightly lower, it is a solid choice for budget-conscious diners.
---
Overall Summary: Spice Garden is the top pick, offering the best combination of cuisine quality, rating, and budget alignment."""

def test_parse_recommendations():
    result = parse_llm_response(SAMPLE_RESPONSE)
    assert len(result.recommendations) == 2
    assert result.recommendations[0].rank == 1
    assert result.recommendations[0].restaurant_name == "Spice Garden"
    assert "4.3" in result.recommendations[0].explanation

def test_parse_summary():
    result = parse_llm_response(SAMPLE_RESPONSE)
    assert "Spice Garden" in result.summary
