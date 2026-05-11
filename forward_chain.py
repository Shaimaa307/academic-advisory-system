from typing import Any
from knowledge_base.rules import Rule, build_rules

def _eval(fact_base: dict, key: str, op: str, value: Any) -> bool:
    if key not in fact_base: return False
    a = fact_base[key]
    try:
        if op == "==": return a == value
        if op == "!=": return a != value
        if op == ">=": return float(a) >= float(value)
        if op == "<=": return float(a) <= float(value)
        if op == ">":  return float(a) >  float(value)
        if op == "<":  return float(a) <  float(value)
        if op == "in": return a in value
    except: pass
    return False

def _apply(fact_base: dict, rule: Rule) -> list[str]:
    lines = []
    for key, val in rule.conclusions:
        if key in ("recommend_course", "recommend_course2"):
            pool = fact_base.setdefault("recommended_courses", [])
            if val not in pool:
                pool.append(val)
                lines.append(f"recommended_courses  ←  '{val}'")
        else:
            fact_base[key] = val
            lines.append(f"{key}  =  {val!r}")
    return lines

class ForwardChainEngine:
    def __init__(self) -> None:
        self._rules = []
        self._fact_base = {}
        self._fired = []
        self._trace = []

    def load(self, facts: dict[str, Any]) -> None:
        self._rules = build_rules()
        self._fact_base = dict(facts)
        self._fired = []
        self._trace = []
        gpa = float(self._fact_base.get("gpa", 2.0))
        courses = float(self._fact_base.get("courses_this_semester", 4))
        self._fact_base["stress_index"] = round((courses / 8.0) * (1.0 - gpa / 4.0), 3)

        self._trace.append("=" * 50)
        self._trace.append("  INITIAL STUDENT DATA")
        self._trace.append("=" * 50)
        for k, v in self._fact_base.items():
            self._trace.append(f"  {k:<20} : {v!r}")

    def run(self) -> dict[str, Any]:
        self._trace.append("\n" + "=" * 50)
        self._trace.append("  INFERENCE ENGINE START")
        self._trace.append("=" * 50)
        while True:
            new = False
            for rule in self._rules:
                if rule.fired: continue
                if all(_eval(self._fact_base, k, op, v) for k, op, v in rule.conditions):
                    rule.fired = True
                    new = True
                    self._fired.append(rule)
                    self._trace.append(f"\n[!] FIRED: {rule.name}")
                    self._trace.append(f"    Reason: {rule.explanation}")
                    for d in _apply(self._fact_base, rule):
                        self._trace.append(f"    Fact Added: {d}")
            if not new: break
        return self._fact_base

    def get_trace(self) -> list[str]: return self._trace

    def summary(self) -> dict[str, Any]:
        fb = self._fact_base
        return {
            "standing": fb.get("standing_label", "Unknown"),
            "level": fb.get("level_label", "Unknown"),
            "is_honors": fb.get("is_honors", False),
            "career_track": fb.get("career_track", "General"),
            "recommendations": fb.get("recommended_courses", []),
            "stress_index": fb.get("stress_index", 0.0),
            "stress_level": fb.get("stress_level", "Normal")
        }