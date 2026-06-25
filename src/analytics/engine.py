"""Compute organization-wide analytics metrics per tick."""


def compute_analytics(org) -> None:
    """Compute all analytics metrics for the current tick."""
    alive_depts = [d for d in org.departments.values() if d.headcount > 0]
    
    if not alive_depts:
        return
    
    m = org.metrics
    m.org_efficiency = sum(d.efficiency for d in alive_depts) / len(alive_depts)
    
    rd_dept = org.departments.get("rd")
    m.innovation_rate = rd_dept.innovation_score if rd_dept else 0.0
    
    m.conflict_score = sum(d.conflict_index for d in alive_depts) / len(alive_depts)
    m.market_adaptability = (org.market.demand_index + (1 - org.market.competitor_pressure)) / 2
    
    total_budget = sum(d.budget for d in alive_depts)
    m.capital_efficiency = min(1.0, total_budget / max(1, org.credits))
