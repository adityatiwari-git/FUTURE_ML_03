"""Synthetic, fictional profiles for reproducible demos and tests."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESUME_DIR = ROOT / "data" / "sample_resumes"

JOBS = {
    "Junior Data Analyst": {
        "description": "Analyze business data using Python, SQL, pandas, NumPy, statistics and data visualization. Machine learning is a plus.",
        "required": ["Python", "SQL", "pandas", "NumPy", "statistics", "data visualization"],
        "preferred": ["machine learning", "scikit-learn", "Excel"],
    },
    "Junior NLP Engineer": {
        "description": "Build text processing and NLP prototypes using Python, machine learning, scikit-learn, NLP and deep learning.",
        "required": ["Python", "machine learning", "NLP", "scikit-learn"],
        "preferred": ["deep learning", "PyTorch", "TensorFlow"],
    },
    "Frontend Developer": {
        "description": "Develop responsive interfaces using HTML, CSS, JavaScript, React and Git.",
        "required": ["HTML", "CSS", "JavaScript", "React", "Git"],
        "preferred": ["TypeScript", "communication"],
    },
}

def load_sample_candidates():
    candidates = []
    for path in sorted(RESUME_DIR.glob("*.txt")):
        candidates.append({"candidate_id": path.stem, "text": path.read_text(encoding="utf-8")})
    return candidates
