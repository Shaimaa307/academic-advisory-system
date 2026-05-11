"""knowledge_base — rules, ontology, and default facts."""
from .rules    import Rule, build_rules, DEFAULT_FACTS
from .ontology import CLASSES, OBJECT_PROPERTIES, DATA_PROPERTIES, DL_AXIOMS

__all__ = [
    "Rule", "build_rules", "DEFAULT_FACTS",
    "CLASSES", "OBJECT_PROPERTIES", "DATA_PROPERTIES", "DL_AXIOMS",
]