"""Agent base class, roles, and memory system."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class AgentRole(Enum):
    CEO = "ceo"
    CFO = "cfo"
    CTO = "cto"
    CMO = "cmo"
    CHRO = "chro"
    ENGINEER = "engineer"
    ANALYST = "analyst"
    MARKETER = "marketer"
    RECRUITER = "recruiter"


class DeptType(Enum):
    EXECUTIVE = "executive"
    FINANCE = "finance"
    RD = "rd"
    MARKETING = "marketing"
    HR = "hr"


@dataclass
class Agent:
    """An autonomous agent within a department."""
    id: str
    name: str
    role: AgentRole
    department: DeptType
    level: int = 1
    morale: float = 0.8
    skill: float = 0.5
    salary: float = 100.0
    memory: list = field(default_factory=list)
    alive: bool = True
    age: int = 0
    actions_completed: int = 0

    def remember(self, action: str, outcome: float) -> None:
        """Record action outcome in memory buffer (max 20)."""
        self.memory.append({"action": action, "outcome": outcome, "age": self.age})
        if len(self.memory) > 20:
            self.memory = self.memory[-20:]

    def avg_outcome(self) -> float:
        """Average outcome of last 10 actions."""
        if not self.memory:
            return 0.5
        recent = self.memory[-10:]
        return sum(m["outcome"] for m in recent) / len(recent)

    def exec_summary(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value,
            "department": self.department.value,
            "level": self.level,
            "morale": round(self.morale, 3),
            "skill": round(self.skill, 3),
            "salary": self.salary,
            "alive": self.alive,
            "age": self.age,
            "actions": self.actions_completed,
            "avg_outcome": round(self.avg_outcome(), 3),
        }
