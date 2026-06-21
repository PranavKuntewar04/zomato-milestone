import re
from dataclasses import dataclass, field

@dataclass
class Recommendation:
    rank: int
    restaurant_name: str
    explanation: str

@dataclass
class RecommendationList:
    recommendations: list[Recommendation] = field(default_factory=list)
    summary: str = ""


def parse_llm_response(raw_response: str) -> RecommendationList:
    """
    Parse the structured LLM response into a RecommendationList.
    Expected format:
        Rank N: [Restaurant Name]
        Explanation: [text]
        ...
        Overall Summary: [text]
    """
    result = RecommendationList()

    # Extract overall summary
    summary_match = re.search(r"Overall Summary:\s*(.+?)(?:\n|$)", raw_response, re.IGNORECASE | re.DOTALL)
    if summary_match:
        result.summary = summary_match.group(1).strip()

    # Extract ranked entries
    rank_pattern = re.findall(
        r"Rank\s+(\d+):\s*(.+?)\nExplanation:\s*(.+?)(?=\n\nRank|\nOverall Summary|---|\Z)",
        raw_response,
        re.DOTALL | re.IGNORECASE,
    )

    for rank_str, name, explanation in rank_pattern:
        result.recommendations.append(
            Recommendation(
                rank=int(rank_str),
                restaurant_name=name.strip(),
                explanation=explanation.strip(),
            )
        )

    return result
