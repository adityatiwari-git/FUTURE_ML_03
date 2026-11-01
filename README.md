# RoleFit — Resume / Candidate Screening System

**Future Interns · Machine Learning Task 3**

RoleFit is an explainable resume-screening prototype. Given a job description and a pool of resumes, it extracts text, identifies skills, compares evidence against required and preferred skills, ranks candidates, and highlights potential skill gaps.

> **Responsible-use notice:** This is a learning and decision-support prototype, not an automated hiring system. A role-fit score is not a probability of success, a measure of candidate quality, or a recommendation to hire. A human reviewer must assess candidates fairly and independently.

## Task requirements addressed

| Future Interns requirement | Implementation |
|---|---|
| Resume text cleaning and parsing | PDF, DOCX and TXT text extraction; normalized skill aliases |
| Skill extraction and matching | Configurable canonical skill taxonomy and alias matching |
| Candidate ranking based on role fit | Required-skill coverage + TF-IDF cosine similarity + preferred-skill coverage |
| Skill-gap identification | Candidate-level matched and missing required skills |
| Deliverable | CLI workflow and interactive Streamlit application |

## Features

- Upload multiple PDF, DOCX or TXT resumes; uploaded bytes are processed in memory and are not written to disk by the app.
- Select a built-in role template (Data Analyst, NLP Engineer, Frontend Developer) or enter a custom job description.
- Edit required and preferred skills for each vacancy.
- Extract canonical skills using an editable alias dictionary in src/skills.py.
- Rank candidates using a transparent, configurable score.
- Inspect candidate-level evidence, including matched skills, missing requirements, extracted skills and explicitly stated experience.
- Export the ranked shortlist as CSV.
- Run a deterministic synthetic ranking benchmark using NDCG@5 and Mean Reciprocal Rank (MRR).

## Scoring methodology

The default role-fit indicator is:

\[
Score = 100 \times (0.70R + 0.20T + 0.10P)
\]

Where:
- \(R\) = proportion of required skills detected in the resume.
- \(T\) = TF-IDF cosine similarity between the job description and resume.
- \(P\) = proportion of preferred skills detected in the resume.

Required skills carry the largest weight. The weights are transparent and can be adapted in src/matcher.py. This is a deterministic ranking heuristic with a TF-IDF information-retrieval component; it is **not** a supervised model trained on historical hiring outcomes. The score must not be described as a probability or used as a pass/fail threshold.

Skill extraction is dictionary/alias-based, not a general-purpose NER model. Extend the taxonomy for the occupation and validate it with domain experts. The parser extracts text from digital PDFs; scanned image-only PDFs may require OCR and are reported when no text is available.

## Synthetic demonstration data and evaluation

The repository contains six fictional demonstration resumes. They contain no real candidate information and are intended only to make the workflow reproducible without collecting personal data.

Run python src/evaluate.py to evaluate the ranking on three roles using manually assigned graded relevance labels for these fictional profiles. It reports NDCG@5 and MRR. These are **synthetic smoke-benchmark metrics**, not independent validation, not evidence of hiring validity, and not representative of real applicant populations. The labels are included transparently in src/evaluate.py.

No real resume corpus is redistributed or required. For any real evaluation, use consented, lawfully obtained, anonymized data with documented annotation procedures and a representative test set.

## Repository structure

~~~text
FUTURE_ML_03/
├── app.py
├── src/
│   ├── skills.py
│   ├── parser.py
│   ├── matcher.py
│   ├── sample_data.py
│   ├── rank_candidates.py
│   └── evaluate.py
├── data/sample_resumes/       # fictional profiles only
├── tests/test_screening.py
├── reports/                   # generated evaluation JSON
├── .github/workflows/tests.yml
└── requirements.txt
~~~

## Setup

Python 3.10+ is recommended.

~~~bash
python -m venv .venv
~~~

Windows PowerShell:

~~~powershell
.venv\Scripts\Activate.ps1
~~~

macOS/Linux:

~~~bash
source .venv/bin/activate
~~~

Install dependencies:

~~~bash
pip install -r requirements.txt
~~~

## Run the application

~~~bash
streamlit run app.py
~~~

1. Choose a role template or enter a custom job description.
2. Review/edit required and preferred skills.
3. Upload resumes or use the fictional demo candidates.
4. Select **Rank candidates**.
5. Review the ranking and evidence, then export the CSV if needed.

## Run the CLI and evaluation

~~~bash
python src/rank_candidates.py
python src/evaluate.py
python -m unittest discover -s tests -v
python -m compileall -q src app.py
~~~

## Demonstration ranking results

The GitHub Actions benchmark on the six fictional profiles produced the following results:

| Role | NDCG@5 | MRR |
|---|---:|---:|
| Junior Data Analyst | 1.0000 | 1.0000 |
| Junior NLP Engineer | 0.9341 | 1.0000 |
| Frontend Developer | 1.0000 | 1.0000 |
| **Mean** | **0.9780** | **1.0000** |

These scores measure agreement with the small, manually authored synthetic relevance table in src/evaluate.py. They are a reproducibility/smoke check only. They must not be interpreted as accuracy on real resumes or evidence of fair, valid or predictive hiring decisions. The evaluation JSON is uploaded as a GitHub Actions artifact for inspection.

## Privacy, fairness and limitations

- Do not upload or commit real resumes unless you have an appropriate lawful basis, candidate permission where required, and organizational approval.
- Uploaded files are processed in memory by this app; the code does not persist them. Hosting providers may have their own request and infrastructure logs.
- The system intentionally does not extract or score names, age, gender, ethnicity, photographs, addresses or other protected/sensitive attributes.
- Skills absent from extracted text may still be held by a candidate. A missing match is not proof of a missing capability.
- Parsing quality depends on document layout, text extraction and the configured vocabulary. OCR, multilingual support, synonym expansion and contextual skill disambiguation are not implemented.
- TF-IDF is lexical and may miss semantically equivalent wording.
- Synthetic evaluation is only a software demonstration. It cannot establish fairness, validity, predictive performance or generalization.
- Before any real use, conduct legal/privacy review, accessibility review, job-related validation, subgroup impact assessment, human oversight and an appeal/correction process.

## References

- Green, T. A. F., Maynard, D., & Lin, C. (2022). *Development of a Benchmark Corpus to Support Entity Recognition in Job Descriptions*. LREC 2022. https://aclanthology.org/2022.lrec-1.128/
- Scikit-learn documentation: https://scikit-learn.org/stable/
- Streamlit documentation: https://docs.streamlit.io/

Built for Future Interns Machine Learning Task 3.
