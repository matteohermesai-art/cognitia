"""Tick engine: executes simulation steps, manages organization lifecycle."""
import random
from typing import Optional
from .state import OrganizationState


def create_organization(name: str = "Cognitia Corp", seed: int = 42,
                        credits: float = 100000.0) -> OrganizationState:
    """Initialize a new organization with departments and agents."""
    random.seed(seed)
    
    from agents.models import Agent, AgentRole, DeptType
    from market import MarketState
    
    org = OrganizationState(credits=credits)
    org.market = MarketState()
    
    # ─── Seed Departments ───
    dept_configs = [
        (DeptType.EXECUTIVE.value, "Executive Office", 15000, [
            ("ceo", "CEO Alpha", AgentRole.CEO, 5, 0.9, 500),
        ]),
        (DeptType.FINANCE.value, "Finance", 12000, [
            ("cfo", "CFO Beta", AgentRole.CFO, 4, 0.85, 400),
            ("analyst1", "Analyst Gamma", AgentRole.ANALYST, 2, 0.6, 150),
        ]),
        (DeptType.RD.value, "R&D", 25000, [
            ("cto", "CTO Delta", AgentRole.CTO, 5, 0.95, 450),
            ("eng1", "Engineer E-1", AgentRole.ENGINEER, 2, 0.7, 120),
            ("eng2", "Engineer E-2", AgentRole.ENGINEER, 3, 0.8, 140),
            ("eng3", "Engineer E-3", AgentRole.ENGINEER, 1, 0.4, 100),
        ]),
        (DeptType.MARKETING.value, "Marketing", 18000, [
            ("cmo", "CMO Zeta", AgentRole.CMO, 4, 0.8, 380),
            ("mkt1", "Marketer Eta", AgentRole.MARKETER, 2, 0.55, 100),
        ]),
        (DeptType.HR.value, "Human Resources", 10000, [
            ("chro", "CHRO Theta", AgentRole.CHRO, 4, 0.75, 350),
            ("rec1", "Recruiter Iota", AgentRole.RECRUITER, 2, 0.5, 90),
        ]),
    ]
    
    from ..departments import Department
    
    for dt, name, budget, agents_cfg in dept_configs:
        dept = Department(dept_type=dt, name=name, budget=budget)
        for aid, aname, role, level, skill, salary in agents_cfg:
            dept.agents.append(Agent(
                id=aid, name=aname, role=role,
                department=DeptType(dt), level=level, skill=skill, salary=salary,
            ))
        org.departments[dt] = dept
    
    return org


def execute_tick(org: OrganizationState) -> None:
    """Execute one simulation tick."""
    org.tick += 1
    
    # 1. Market update
    org.market.update()
    
    # 2. Department decisions (order matters: CEO -> Finance -> others)
    from departments import ceo_decision, finance_decision, rd_decision, marketing_decision, hr_decision
    from analytics.engine import compute_analytics
    from economy import compute_revenue
    
    ceo_decision(org)
    finance_decision(org)
    rd_decision(org)
    marketing_decision(org)
    hr_decision(org)
    
    # 3. Agent lifecycle (aging, morale decay)
    for dept in org.departments.values():
        for agent in dept.agents:
            if agent.alive:
                agent.age += 1
                agent.actions_completed += 1
                # Natural morale decay
                agent.morale = max(0.0, agent.morale - 0.001)
                # Low salary hurts morale
                if agent.salary < 100 and random.random() < 0.1:
                    agent.morale -= 0.02
    
    # 4. Inter-department conflicts (random)
    if random.random() < 0.1:
        depts = list(org.departments.values())
        if len(depts) >= 2:
            d1, d2 = random.sample(depts, 2)
            d1.conflict_index = min(1.0, d1.conflict_index + random.uniform(0.05, 0.15))
            d2.conflict_index = min(1.0, d2.conflict_index + random.uniform(0.05, 0.15))
    
    # 5. Compute analytics
    compute_analytics(org)
    
    # 6. Record snapshot (every 100 ticks to save memory)
    if org.tick % 100 == 0:
        org.record_tick()
