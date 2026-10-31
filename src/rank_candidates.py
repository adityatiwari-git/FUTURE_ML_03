"""Explainable resume-to-role matching demo using synthetic text profiles."""
from pathlib import Path
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
RESUME_DIR = ROOT / "data" / "sample_resumes"
SKILLS = {
    "python", "sql", "pandas", "numpy", "scikit-learn", "machine learning",
    "data visualization", "statistics", "nlp", "java", "html", "css",
    "javascript", "react", "git", "deep learning", "tensorflow", "pytorch",
}


def extract_skills(text: str) -> set[str]:
    normalized = re.sub(r"[^a-z0-9+#. ]", " ", text.lower())
    return {skill for skill in SKILLS if re.search(
        rf"(?<![a-z0-9+#.]){re.escape(skill)}(?![a-z0-9+#.])", normalized
    )}


def main() -> None:
    job_description = (
        "We seek a junior machine learning analyst with Python, SQL, pandas, "
        "NumPy, scikit-learn, statistics, NLP and data visualization skills."
    )
    required = extract_skills(job_description)
    paths = sorted(RESUME_DIR.glob("*.txt"))
    if not paths:
        raise SystemExit("No demo resumes found in data/sample_resumes/")
    texts = [p.read_text(encoding="utf-8") for p in paths]
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform([job_description] + texts)
    similarities = cosine_similarity(matrix[0:1], matrix[1:]).ravel()

    results = []
    for path, text, similarity in zip(paths, texts, similarities):
        matched = extract_skills(text) & required
        missing = required - matched
        coverage = len(matched) / len(required) if required else 0.0
        # Transparent heuristic: skill coverage is primary; text similarity is secondary.
        score = 100 * (0.8 * coverage + 0.2 * float(similarity))
        results.append((score, path.name, matched, missing))
    for score, name, matched, missing in sorted(results, reverse=True):
        print(f"\n{name}: {score:.1f}/100 (demo match indicator)")
        print("Matched skills:", ", ".join(sorted(matched)) or "None")
        print("Missing listed skills:", ", ".join(sorted(missing)) or "None")
    print("\nReminder: synthetic demo only; scores are not validated hiring assessments.")


if __name__ == "__main__":
    main()
