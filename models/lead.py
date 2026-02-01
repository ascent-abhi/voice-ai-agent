from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Lead:
    pain_points: List[str] = field(default_factory=list)
    current_tool: Optional[str] = None
    authority: Optional[str] = None
    budget: Optional[str] = None
    timeline: Optional[str] = None
    company_size: Optional[str] = None

    qualification: Optional[str] = None  # QUALIFIED / NOT_QUALIFIED
    score: Optional[int] = None
    reasoning: Optional[str] = None
