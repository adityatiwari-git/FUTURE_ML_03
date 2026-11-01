"""Explainable resume parsing, skill matching and candidate ranking."""
from __future__ import annotations
import re
from dataclasses import dataclass, asdict
from typing import Iterable
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.skills import extract_skills, normalize_skill_list

@dataclass
class CandidateMatch:
    candidate_id: str
    score: float
    text_similarity: float
    required_coverage: float
    preferred_coverage: float
    matched_required: list[str]
    missing_required: list[str]
    matched_preferred: list[str]
    extracted_skills: list[str]
    experience_years: float | None

    def to_dict(self):
        return asdict(self)


def extract_experience_years(text: str) -> float | None:
    """Extract explicit total-experience statements; do not infer dates or gaps."""
    patterns = [
        r"(?:total\s+)?(?:experience|work experience)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*\+?\s*(?:years|yrs)",
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years|yrs)\s+(?:of\s+)?experience",
    ]
    values = []
    for pattern in patterns:
        values.extend(float(x) for x in re.findall(pattern, text or "", flags=re.IGNORECASE))
    return max(values) if values else None


def match_candidate(candidate_id: str, resume_text: str, job_description: str,
                    required_skills: Iterable[str] | None = None,
                    preferred_skills: Iterable[str] | None = None) -> CandidateMatch:
    resume = resume_text or ""
    job = job_description or ""
    resume_skills = extract_skills(resume)
    required = normalize_skill_list(required_skills or extract_skills(job))
    preferred = normalize_skill_list(preferred_skills or [])
    matched_required = resume_skills & required
    matched_preferred = resume_skills & preferred
    missing = required - matched_required
    req_coverage = len(matched_required) / len(required) if required else 1.0
    pref_coverage = len(matched_preferred) / len(preferred) if preferred else 0.0

    if not resume.strip() or not job.strip():
        similarity = 0.0
    else:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
        matrix = vectorizer.fit_transform([job, resume])
        similarity = float(cosine_similarity(matrix[0:1], matrix[1:2])[0, 0])

    # Transparent role-fit indicator: required skills dominate; semantic text similarity
    # and preferred skills are secondary. This is not a probability or hiring verdict.
    score = 100.0 * (0.70 * req_coverage + 0.20 * similarity + 0.10 * pref_coverage)
    return CandidateMatch(
        candidate_id=candidate_id, score=round(score, 2),
        text_similarity=round(similarity, 4),
        required_coverage=round(req_coverage, 4),
        preferred_coverage=round(pref_coverage, 4),
        matched_required=sorted(matched_required),
        missing_required=sorted(missing),
        matched_preferred=sorted(matched_preferred),
        extracted_skills=sorted(resume_skills),
        experience_years=extract_experience_years(resume),
    )


def rank_candidates(candidates: Iterable[dict], job_description: str,
                    required_skills: Iterable[str] | None = None,
                    preferred_skills: Iterable[str] | None = None) -> list[CandidateMatch]:
    results = [
        match_candidate(str(item["candidate_id"]), str(item["text"]), job_description,
                        required_skills, preferred_skills)
        for item in candidates
    ]
    return sorted(results, key=lambda item: (-item.score, item.candidate_id))
