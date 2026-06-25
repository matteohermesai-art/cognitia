"""Department models and decision functions for all 5 departments."""
from dataclasses import dataclass, field
import random


@dataclass
class Department:
    """A department within the organization."""
    dept_type: str
    name: str
    budget: float = 10000.0
    agents: list = field(default_factory=list)
    efficiency: float = 0.5
    innovation_score: float = 0.0
    conflict_index: float = 0.0

    @property
    def headcount(self) -> int:
        return len([a for a in self.agents if a.alive])

    @property
    def avg_morale(self) -> float:
        alive = [a for a in self.agents if a.alive]
        return sum(a.morale for a in alive) / len(alive) if alive else 0.0

    @property
    def burn_rate(self) -> float:
        return sum(a.salary for a in self.agents if a.alive) / 100

    @property
    def avg_skill(self) -> float:
        alive = [a for a in self.agents if a.alive]
        return sum(a.skill for a in alive) / len(alive) if alive else 0.0


def ceo_decision(org) -> dict:
    """Executive: allocate budgets and resolve conflicts."""
    total_budget = org.credits * 0.15
    weights = {}
    for dt, dept in org.departments.items():
        perf = dept.efficiency * 0.4 + dept.avg_morale * 0.3 + dept.innovation_score * 0.3
        weights[dt] = max(0.1, perf)
    total_weight = sum(weights.values())
    for dt, dept in org.departments.items():
        dept.budget = total_budget * (weights[dt] / total_weight)
        if dept.conflict_index > 0.7:
            dept.budget *= 0.8
            dept.conflict_index *= 0.9
    return {"action": "budget_allocation", "amount": total_budget}


def finance_decision(org) -> dict:
    """Finance: manage cashflow, compute revenue."""
    from economy import compute_revenue, compute_burn_rate
    org.burn_rate = compute_burn_rate(org)
    org.revenue = compute_revenue(org)
    org.credits += org.revenue
    org.total_revenue += max(0, org.revenue)
    return {"action": "finance_update", "revenue": org.revenue}


def rd_decision(org) -> dict:
    """R&D: generate innovation, improve product-market fit."""
    dept = org.departments.get("rd")
    if not dept:
        return {"action": "rd_cycle", "error": "no rd department"}
    budget_factor = min(1.0, dept.budget / 20000)
    skill_avg = dept.avg_skill
    delta = skill_avg * budget_factor * 0.05 * random.uniform(0.8, 1.2)
    dept.innovation_score = min(1.0, dept.innovation_score + delta)
    if dept.innovation_score > org.market.product_market_fit:
        org.market.product_market_fit = min(1.0, org.market.product_market_fit + delta * 0.3)
    dept.budget -= dept.burn_rate
    for a in dept.agents:
        if a.alive and random.random() < 0.1:
            a.skill = min(1.0, a.skill + random.uniform(0.01, 0.05))
    return {"action": "rd_cycle", "innovation_score": dept.innovation_score}


def marketing_decision(org) -> dict:
    """Marketing: drive demand, counter competition."""
    dept = org.departments.get("marketing")
    if not dept:
        return {"action": "marketing_cycle", "error": "no marketing department"}
    budget_factor = min(1.0, dept.budget / 15000)
    skill_avg = dept.avg_skill
    org.market.demand_index = min(1.0, max(0.0, org.market.demand_index + skill_avg * budget_factor * 0.03))
    org.market.competitor_pressure = max(0.0, org.market.competitor_pressure - skill_avg * 0.01)
    dept.efficiency = min(1.0, dept.efficiency + random.uniform(-0.02, 0.03))
    dept.budget -= dept.burn_rate
    return {"action": "marketing_cycle", "demand": org.market.demand_index}


def hr_decision(org) -> dict:
    """HR: manage hiring, morale, attrition."""
    dept = org.departments.get("hr")
    if not dept:
        return {"action": "hr_cycle", "error": "no hr department"}
    from agents.models import Agent, AgentRole, DeptType
    role_map = {
        "finance": AgentRole.ANALYST,
        "rd": AgentRole.ENGINEER,
        "marketing": AgentRole.MARKETER,
        "hr": AgentRole.RECRUITER,
    }
    for dt, d in org.departments.items():
        if d.avg_morale < 0.4:
            d.conflict_index *= 0.95
            for a in d.agents:
                a.morale = min(1.0, a.morale + 0.05)
    for dt, d in org.departments.items():
        for a in d.agents:
            if a.alive and a.morale < 0.3 and random.random() < 0.05:
                a.alive = False
                a.morale = 0.0
    for dt, d in org.departments.items():
        if d.headcount < 3 and org.credits > 5000:
            new_id = f"{dt[:2]}_hire_{random.randint(1000, 9999)}"
            d.agents.append(Agent(
                id=new_id,
                name=f"Hire-{new_id[-4:]}",
                role=role_map.get(dt, AgentRole.ANALYST),
                department=DeptType(dt),
                level=1,
                skill=random.uniform(0.3, 0.5),
                salary=80.0,
            ))
    dept.budget -= dept.burn_rate
    total = sum(d.headcount for d in org.departments.values())
    return {"action": "hr_cycle", "total_headcount": total}
