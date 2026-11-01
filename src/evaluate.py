"""Evaluate ranking on a small, explicitly synthetic relevance-judgement set."""
import json
import math
from pathlib import Path
from src.matcher import rank_candidates
from src.sample_data import JOBS, load_sample_candidates

# Graded relevance labels are manually assigned to fictional profiles for a
# deterministic smoke benchmark. They are not human hiring judgements.
RELEVANCE = {
    "Junior Data Analyst": {
        "candidate_01": 3, "candidate_03": 3, "candidate_05": 3,
        "candidate_04": 1, "candidate_02": 0, "candidate_06": 0,
    },
    "Junior NLP Engineer": {
        "candidate_04": 3, "candidate_03": 3, "candidate_01": 1,
        "candidate_02": 0, "candidate_05": 0, "candidate_06": 0,
    },
    "Frontend Developer": {
        "candidate_02": 3, "candidate_06": 3, "candidate_01": 0,
        "candidate_03": 0, "candidate_04": 0, "candidate_05": 0,
    },
}


def ndcg_at_k(ranked_ids, relevance, k=5):
    gains = [((2 ** relevance.get(cid, 0)) - 1) / math.log2(i + 2)
             for i, cid in enumerate(ranked_ids[:k])]
    ideal = sorted(relevance.values(), reverse=True)[:k]
    ideal_gains = [((2 ** rel) - 1) / math.log2(i + 2)
                   for i, rel in enumerate(ideal)]
    denominator = sum(ideal_gains)
    return sum(gains) / denominator if denominator else 0.0


def reciprocal_rank(ranked_ids, relevance):
    for index, cid in enumerate(ranked_ids, start=1):
        if relevance.get(cid, 0) > 0:
            return 1.0 / index
    return 0.0


def main():
    candidates = load_sample_candidates()
    per_role = {}
    for role, job in JOBS.items():
        ranked = rank_candidates(candidates, job["description"], job["required"], job["preferred"])
        ids = [item.candidate_id for item in ranked]
        per_role[role] = {
            "ndcg_at_5": round(ndcg_at_k(ids, RELEVANCE[role], 5), 4),
            "mrr": round(reciprocal_rank(ids, RELEVANCE[role]), 4),
            "ranking": ids,
        }
    summary = {
        "evaluation_type": "synthetic demonstration benchmark",
        "candidate_count": len(candidates),
        "role_count": len(JOBS),
        "mean_ndcg_at_5": round(sum(x["ndcg_at_5"] for x in per_role.values()) / len(per_role), 4),
        "mean_reciprocal_rank": round(sum(x["mrr"] for x in per_role.values()) / len(per_role), 4),
        "per_role": per_role,
        "limitation": "Fictional resumes and manually assigned synthetic relevance labels; not evidence of real-world hiring validity.",
    }
    output = Path(__file__).resolve().parents[1] / "reports"
    output.mkdir(exist_ok=True)
    (output / "ranking_evaluation.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
