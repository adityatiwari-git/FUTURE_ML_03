"""Streamlit UI for privacy-conscious, explainable resume-to-role screening."""
import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.matcher import rank_candidates
from src.parser import extract_text_from_bytes
from src.sample_data import JOBS, load_sample_candidates

st.set_page_config(page_title="RoleFit | Candidate Screening", page_icon="🧭", layout="wide")
st.title("🧭 RoleFit — Resume & Candidate Screening")
st.caption("Explainable skill matching, role-fit ranking and skill-gap analysis")
st.info("Decision-support prototype only. Scores are not hiring probabilities or automated decisions. Review every candidate fairly and independently.")

with st.sidebar:
    st.header("Job requirements")
    role_choice = st.selectbox("Start with a role template", ["Custom role", *JOBS.keys()])
    if role_choice == "Custom role":
        default_description = ""
        default_required = ""
        default_preferred = ""
    else:
        selected = JOBS[role_choice]
        default_description = selected["description"]
        default_required = ", ".join(selected["required"])
        default_preferred = ", ".join(selected["preferred"])
    job_description = st.text_area("Job description", value=default_description, height=180)
    required_text = st.text_input("Required skills (comma-separated)", value=default_required)
    preferred_text = st.text_input("Preferred skills (comma-separated)", value=default_preferred)

st.subheader("Add candidate resumes")
uploaded = st.file_uploader("Upload resumes (PDF, DOCX or TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)
use_demo = st.checkbox("Include fictional demo candidates", value=not bool(uploaded))

candidates = []
errors = []
if use_demo:
    candidates.extend(load_sample_candidates())
for file in uploaded or []:
    try:
        text = extract_text_from_bytes(file.name, file.getvalue())
        if not text.strip():
            errors.append(f"{file.name}: no extractable text found (scanned PDFs may need OCR).")
        else:
            candidates.append({"candidate_id": Path(file.name).stem, "text": text})
    except Exception as exc:
        errors.append(f"{file.name}: {exc}")

for error in errors:
    st.warning(error)

if st.button("Rank candidates", type="primary", disabled=not (job_description.strip() and candidates)):
    required = [x.strip() for x in required_text.split(",") if x.strip()]
    preferred = [x.strip() for x in preferred_text.split(",") if x.strip()]
    ranked = rank_candidates(candidates, job_description, required or None, preferred)
    st.subheader("Ranked shortlist")
    st.caption(f"{len(ranked)} candidate(s) assessed. Ranking is based on declared role requirements and text relevance.")
    table = pd.DataFrame([{
        "Rank": i,
        "Candidate": item.candidate_id,
        "Role-fit indicator": item.score,
        "Required skill coverage": item.required_coverage * 100,
        "Text similarity": item.text_similarity * 100,
        "Missing required skills": ", ".join(item.missing_required) or "None",
    } for i, item in enumerate(ranked, start=1)])
    st.dataframe(table.style.format({
        "Role-fit indicator": "{:.1f}",
        "Required skill coverage": "{:.1f}%",
        "Text similarity": "{:.1f}%",
    }), use_container_width=True, hide_index=True)
    st.bar_chart(table.set_index("Candidate")["Role-fit indicator"])
    st.download_button("Download ranking CSV", table.to_csv(index=False).encode("utf-8"),
                       file_name="candidate_role_fit_results.csv", mime="text/csv")

    st.subheader("Candidate-by-candidate evidence")
    for index, item in enumerate(ranked, start=1):
        with st.expander(f"{index}. {item.candidate_id} — {item.score:.1f}/100"):
            left, right = st.columns(2)
            left.metric("Required skill coverage", f"{item.required_coverage * 100:.1f}%")
            right.metric("Text similarity", f"{item.text_similarity * 100:.1f}%")
            st.write("**Matched required skills:**", ", ".join(item.matched_required) or "None")
            st.write("**Missing required skills:**", ", ".join(item.missing_required) or "None")
            st.write("**Matched preferred skills:**", ", ".join(item.matched_preferred) or "None")
            st.write("**Other extracted skills:**", ", ".join(item.extracted_skills) or "None")
            st.write("**Explicitly stated experience:**",
                     f"{item.experience_years:g} years" if item.experience_years is not None else "Not stated / not detected")
            st.caption("The system reports evidence found in text; absence of a detected skill is not proof the candidate lacks it.")

elif not candidates:
    st.warning("Upload at least one resume or select the fictional demo candidates.")
elif not job_description.strip():
    st.warning("Enter a job description before ranking candidates.")

with st.expander("How the role-fit indicator is calculated"):
    st.markdown("""
    - **70% required-skill coverage:** share of required skills found in the resume.
    - **20% TF-IDF text similarity:** lexical relevance between the job description and resume.
    - **10% preferred-skill coverage:** share of preferred skills found in the resume.

    This is a transparent heuristic, not a trained probability model, validated predictor of job performance, or recommendation to hire. The skill vocabulary is configurable in src/skills.py.
    """)

st.caption("Privacy: uploaded files are processed in memory by this app and are not saved by the project code. Avoid uploading resumes unless you have permission to process them.")
