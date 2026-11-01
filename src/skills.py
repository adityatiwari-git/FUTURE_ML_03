"""Curated, explainable skill taxonomy for the demonstration system."""
import re
from typing import Iterable

# Canonical skill -> common surface forms. Extend for the target occupation.
SKILL_ALIASES = {
    "python": ["python", "python3"],
    "sql": ["sql", "mysql", "postgresql", "postgres"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "statistics": ["statistics", "statistical analysis"],
    "data visualization": ["data visualization", "data visualisation", "tableau", "power bi", "matplotlib", "seaborn"],
    "nlp": ["natural language processing", "nlp"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript"],
    "react": ["react", "react.js"],
    "html": ["html", "html5"],
    "css": ["css", "css3", "tailwind"],
    "git": ["git", "github"],
    "linux": ["linux"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
    "excel": ["excel", "microsoft excel"],
    "communication": ["communication", "stakeholder communication"],
    "project management": ["project management", "agile", "scrum"],
    "biopython": ["biopython"],
    "bioinformatics": ["bioinformatics"],
    "sequence analysis": ["sequence analysis", "sequence alignment"],
    "r": ["r programming", "rstudio"],
}

def _contains_phrase(text: str, phrase: str) -> bool:
    pattern = r"(?<![a-z0-9+#])" + re.escape(phrase) + r"(?![a-z0-9+#])"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def extract_skills(text: str, taxonomy: dict[str, list[str]] | None = None) -> set[str]:
    """Extract canonical skills using boundary-aware aliases, not opaque NER."""
    source = text or ""
    mapping = taxonomy or SKILL_ALIASES
    found = set()
    for canonical, aliases in mapping.items():
        if any(_contains_phrase(source, alias) for alias in aliases):
            found.add(canonical)
    return found


def normalize_skill_list(skills: Iterable[str]) -> set[str]:
    """Normalize user-entered skill names against known canonical terms."""
    mapping = {alias.lower(): canonical for canonical, aliases in SKILL_ALIASES.items()
               for alias in [canonical, *aliases]}
    normalized = set()
    for item in skills:
        key = item.strip().lower()
        if key in mapping:
            normalized.add(mapping[key])
        elif key:
            normalized.add(key)
    return normalized
