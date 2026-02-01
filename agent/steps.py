from enum import Enum, auto


class AgentStep(Enum):
    INTRO = auto()
    PAIN = auto()
    TOOL = auto()
    AUTHORITY = auto()
    BUDGET = auto()
    TIMELINE = auto()
    COMPANY_SIZE = auto()
    JUDGEMENT = auto()
    DONE = auto()
