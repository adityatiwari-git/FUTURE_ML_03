"""Backward-compatible CLI entry point for candidate ranking."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.matcher import rank_candidates
from src.sample_data import JOBS, load_sample_candidates


def main():
    job = JOBS["Junior Data Analyst"]
    ranked = rank_candidates(load_sample_candidates(), job["description"],
                             job["required"], job["preferred"])
    for rank, item in enumerate(ranked, start=1):
        print(f"{rank}. {item.candidate_id}: {item.score:.1f}/100")
        print("   Matched:", ", ".join(item.matched_required) or "None")
        print("   Missing:", ", ".join(item.missing_required) or "None")
    print("\nScores are explainable demo indicators, not probabilities or hiring decisions.")


if __name__ == "__main__":
    main()
