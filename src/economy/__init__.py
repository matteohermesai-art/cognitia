"""Economy module: revenue, burn rate, budget tracking."""
import random


def compute_revenue(org) -> float:
    """Compute tick revenue from marketing and R&D."""
    mkt = org.departments.get("marketing")
    rd = org.departments.get("rd")
    base_rev = (mkt.efficiency if mkt else 0) * 5000 * org.market.demand_index
    innov_bonus = (rd.innovation_score if rd else 0) * 3000
    revenue = base_rev + innov_bonus - org.market.competitor_pressure * 2000
    # External shock effects
    if org.market.external_shock == "crash": revenue *= 0.5
    elif org.market.external_shock == "opportunity": revenue *= 1.5
    elif org.market.external_shock == "regulation": revenue *= 0.8
    return revenue


def compute_burn_rate(org) -> float:
    """Compute total burn rate across all departments."""
    return sum(d.burn_rate for d in org.departments.values())


def compute_roi(org, dept_type: str) -> float:
    """Compute ROI for a specific department."""
    dept = org.departments.get(dept_type)
    if not dept or dept.burn_rate == 0:
        return 0.0
    if dept_type == "marketing":
        return (org.revenue * 0.4) / max(1, dept.burn_rate * 100)
    elif dept_type == "rd":
        return (org.revenue * 0.3) / max(1, dept.burn_rate * 100)
    return 0.1
