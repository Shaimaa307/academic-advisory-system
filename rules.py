
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Rule:
    id:           str
    name:         str
    category:     str 
    chain_level:  int 
    conditions:   list 
    conclusions:  list 
    explanation:  str
    fired:        bool = field(default=False, init=False)

    def reset(self) -> None:
        self.fired = False

    def __repr__(self) -> str:
        return f"<Rule {self.id} | {self.category} | L{self.chain_level} | {'FIRED' if self.fired else 'ready'}>"

DEFAULT_FACTS: dict[str, Any] = {
    "gpa":                   2.5,
    "total_credits":           60,
    "courses_this_semester":  4,
    "failed_courses":         0,
    "years_enrolled":         3,
    "missing_prereqs":        0,
    "career_interest":        "software",
    "financial_aid":          False,
    "core_courses_done":      False,
    "failed_core_course":     False,
    "needs_math":             False,
    "medical_emergency":      False,
    "request_overload":       False,
}

def build_rules() -> list[Rule]:
    """Return a fresh list of all production rules including GPA gap fixes."""
    return [

        # --- CATEGORY 1: CLASSIFICATION (GPA & LEVEL) ---

        Rule(
            id="R01", name="Good Academic Standing",
            category="Classification", chain_level=1,
            conditions=[("gpa", ">=", 2.0), ("gpa", "<", 3.0)],
            conclusions=[("academic_standing", "good"),
                         ("standing_label", "Good Standing")],
            explanation="GPA between 2.0 and 2.99: student meets minimum requirements."
        ),
        
        # القاعدة الجديدة لسد الفجوة (Very Good)
        Rule(
            id="R36", name="Very Good Standing",
            category="Classification", chain_level=1,
            conditions=[("gpa", ">=", 3.0), ("gpa", "<", 3.7)],
            conclusions=[("academic_standing", "very_good"),
                         ("standing_label", "Very Good Standing")],
            explanation="GPA between 3.0 and 3.69: student is performing very well."
        ),

        Rule(
            id="R02", name="Dean's List / Honors",
            category="Classification", chain_level=1,
            conditions=[("gpa", ">=", 3.7)],
            conclusions=[("academic_standing", "honors"),
                         ("standing_label", "Dean's List  🏆"),
                         ("is_honors", True)],
            explanation="GPA >= 3.7: student qualifies for honors status."
        ),

        Rule(
            id="R03", name="Academic Warning",
            category="Classification", chain_level=1,
            conditions=[("gpa", ">=", 1.5), ("gpa", "<", 2.0)],
            conclusions=[("academic_standing", "warning"),
                         ("standing_label", "Academic Warning  ⚠")],
            explanation="GPA between 1.5 and 1.99: student is under academic warning."
        ),

        Rule(
            id="R04", name="Academic Probation",
            category="Classification", chain_level=1,
            conditions=[("gpa", "<", 1.5)],
            conclusions=[("academic_standing", "probation"),
                         ("standing_label", "Academic Probation  🚨"),
                         ("on_probation", True)],
            explanation="GPA below 1.5: high risk of dismissal."
        ),

        # --- STUDENT LEVEL RULES (BASED ON CREDITS) ---

        Rule(
            id="R05", name="Freshman (Year 1)",
            category="Classification", chain_level=1,
            conditions=[("total_credits", "<", 30)],
            conclusions=[("student_level", "freshman"),
                         ("level_label", "Freshman  (Year 1)")],
            explanation="Fewer than 30 credits."
        ),
        Rule(
            id="R06", name="Sophomore (Year 2)",
            category="Classification", chain_level=1,
            conditions=[("total_credits", ">=", 30), ("total_credits", "<", 60)],
            conclusions=[("student_level", "sophomore"),
                         ("level_label", "Sophomore  (Year 2)")],
            explanation="30–59 credits."
        ),
        Rule(
            id="R07", name="Junior (Year 3)",
            category="Classification", chain_level=1,
            conditions=[("total_credits", ">=", 60), ("total_credits", "<", 90)],
            conclusions=[("student_level", "junior"),
                         ("level_label", "Junior  (Year 3)")],
            explanation="60–89 credits."
        ),
        Rule(
            id="R08", name="Senior (Year 4)",
            category="Classification", chain_level=1,
            conditions=[("total_credits", ">=", 90)],
            conclusions=[("student_level", "senior"),
                         ("level_label", "Senior  (Year 4)")],
            explanation="90+ credits."
        ),

        # --- DIAGNOSIS & REASONING (LEVEL 2 & 3) ---

        Rule(
            id="R10", name="At-Risk (Combined)",
            category="Diagnosis", chain_level=2,
            conditions=[("academic_standing", "==", "warning"),
                        ("total_credits", "<", 60)],
            conclusions=[("at_risk", True),
                         ("risk_reason", "Low GPA + Early Stage")],
            explanation="Early stage students with warnings are flagged as at-risk."
        ),
        
        Rule(
            id="R13", name="Graduation Jeopardized",
            category="Diagnosis", chain_level=3,
            conditions=[("student_level", "==", "senior"),
                        ("at_risk", "==", True)],
            conclusions=[("graduation_at_risk", True),
                         ("escalate_to_advisor", True)],
            explanation="Seniors at risk require immediate intervention."
        ),

        # --- RECOMMENDATIONS & TRACKS ---

        Rule(
            id="R21", name="Software Engineering Track",
            category="Recommendation", chain_level=1,
            conditions=[("career_interest", "==", "software"),
                        ("student_level", "in", ["freshman", "sophomore"])],
            conclusions=[("recommend_course",  "CS101 — Intro to Programming"),
                         ("recommend_course2", "CS201 — Data Structures & Algorithms")],
            explanation="Early recommendation for software interests."
        ),

        Rule(
            id="R28", name="AI / Deep Learning Track",
            category="Recommendation", chain_level=2,
            conditions=[("gpa", ">=", 3.5),
                        ("career_interest", "==", "ai"),
                        ("student_level", "in", ["junior", "senior"])],
            conclusions=[("recommend_course",  "AI401 — Deep Learning"),
                         ("recommend_course2", "AI402 — Natural Language Processing"),
                         ("career_track", "Artificial Intelligence  🤖")],
            explanation="High GPA seniors interested in AI are guided to DL and NLP."
        ),

        # --- ESCALATION ---
        
        Rule(
            id="R35", name="Mandatory Academic Counseling",
            category="Escalation", chain_level=3,
            conditions=[("needs_counseling", "==", True),
                        ("at_risk", "==", True)],
            conclusions=[("mandatory_counseling",   True),
                         ("counseling_deadline",     "within 7 days"),
                         ("escalation_message",
                          "MANDATORY: Student must book an academic counseling session.")],
            explanation="Critical risk triggers mandatory counseling."
        ),
    ]