# Resume / Candidate Screening | Future Interns ML Task 3

An explainable prototype that compares resume text with a job description, surfaces matching skills, identifies gaps, and ranks candidates by transparent role-related evidence.

## Project status
Starter implementation committed. Demo resumes are synthetic. Do not commit real resumes, contact details, or other personal information.

## Quick start
```bash
python -m venv .venv
pip install -r requirements.txt
python src/rank_candidates.py
```

## Method
- Extract text from plain-text demo resume files.
- Identify skills from a configurable skill vocabulary.
- Compare candidate skill evidence with job requirements.
- Calculate a transparent match score and list matched/missing skills.
- Rank candidates for human review.

The prototype uses TF-IDF/cosine similarity as an additional text relevance signal. It does not infer candidate quality, future performance, or suitability from protected characteristics.

## Structure
```
data/sample_resumes/  # synthetic demo resumes only
src/rank_candidates.py
reports/
requirements.txt
```

## Responsible-use constraints
This is a learning and decision-support prototype, not an automated hiring system. A score must never be the sole basis for employment decisions. Validate job-related criteria with domain experts, audit for disparate impact, provide human review, and obtain appropriate consent for any real resume data. Exclude protected attributes and proxies wherever possible.

## Next steps
Test on a consented, anonymized, representative dataset; document annotation quality; compare ranking methods; and conduct a formal bias and privacy assessment before any real-world use.
