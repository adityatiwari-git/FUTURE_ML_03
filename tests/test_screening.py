import unittest
from src.skills import extract_skills, normalize_skill_list
from src.matcher import match_candidate, rank_candidates, extract_experience_years
from src.parser import extract_text_from_bytes


class SkillExtractionTests(unittest.TestCase):
    def test_extracts_aliases_as_canonical_skills(self):
        found = extract_skills("Built models with Python3, sklearn, PostgreSQL and NLP.")
        self.assertEqual(found, {"python", "scikit-learn", "sql", "nlp"})

    def test_avoids_partial_word_matches(self):
        self.assertNotIn("java", extract_skills("I enjoy JavaScript development."))

    def test_normalizes_user_skill_names(self):
        self.assertEqual(normalize_skill_list(["PostgreSQL", "React.js"]), {"sql", "react"})


class MatchingTests(unittest.TestCase):
    def test_missing_required_skills_are_reported(self):
        result = match_candidate("candidate-a", "Python and pandas projects",
                                 "Python SQL pandas analyst role", ["Python", "SQL", "pandas"])
        self.assertEqual(result.matched_required, ["pandas", "python"])
        self.assertEqual(result.missing_required, ["sql"])
        self.assertAlmostEqual(result.required_coverage, 2 / 3)

    def test_ranking_is_descending_and_deterministic(self):
        job = "Python SQL pandas statistics data visualization"
        candidates = [
            {"candidate_id": "weak", "text": "HTML CSS React frontend"},
            {"candidate_id": "strong", "text": "Python SQL pandas statistics data visualization"},
        ]
        ranked = rank_candidates(candidates, job, ["Python", "SQL", "pandas"])
        self.assertEqual(ranked[0].candidate_id, "strong")
        self.assertGreaterEqual(ranked[0].score, ranked[1].score)

    def test_experience_requires_explicit_statement(self):
        self.assertEqual(extract_experience_years("Work experience: 2.5 years"), 2.5)
        self.assertIsNone(extract_experience_years("Worked on projects during college."))


class ParsingTests(unittest.TestCase):
    def test_txt_parser(self):
        self.assertEqual(extract_text_from_bytes("resume.txt", b"Python developer"), "Python developer")

    def test_unsupported_file_type(self):
        with self.assertRaises(ValueError):
            extract_text_from_bytes("resume.png", b"not a resume")


if __name__ == "__main__":
    unittest.main()
