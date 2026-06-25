"""Cognitia — Autonomous Corporate Evolution Engine

Main entry point for running the simulation.
"""
import sys
import os

# Ensure src/ is in path
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
else:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

import asyncio
import random
import time
import json
from datetime import datetime


def create_organization(seed: int = 42, credits: float = 100000.0):
    """Initialize the organization with all departments and agents."""
    random.seed(seed)
    
    from core_engine.state import OrganizationState, TickMetrics
    from agents.models import Agent, AgentRole, DeptType
    from market import MarketState
    from departments import Department
    
    org = OrganizationState(credits=credits)
    org.market = MarketState()
    
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
            ("eng1", "Engineer E-1", AgentRole.ENGINEER, 3, 0.7, 120),
            ("eng2", "Engineer E-2", AgentRole.ENGINEER, 2, 0.65, 110),
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
    
    for dt, name, budget, agents_cfg in dept_configs:
        dept = Department(dept_type=dt, name=name, budget=budget)
        for aid, aname, role, level, skill, salary in agents_cfg:
            dept.agents.append(Agent(
                id=aid, name=aname, role=role,
                department=DeptType(dt), level=level, skill=skill, salary=salary,
            ))
        org.departments[dt] = dept
    
    return org


def execute_tick(org):
    """Execute one simulation tick."""
    from core_engine.tick import execute_tick as _execute
    _execute(org)


def print_banner(config):
    print("=" * 72)
    print("  COGNITIA — Autonomous Corporate Evolution Engine v1.0")
    print("=" * 72)
    print(f"  Seed: {config['seed']}")
    print(f"  Initial Credits: {config['initial_credits']:,.0f} C-credits")
    print(f"  Total Ticks: {config['total_ticks']}")
    print("=" * 72)
    print()


def print_final_report(org, elapsed):
    print("\n" + "=" * 72)
    print(f"  REPORT FINALE — {org.tick} TICK — {elapsed:.1f}s")
    print("=" * 72)
    
    total_agents = sum(d.headcount for d in org.departments.values())
    print(f"\n  AGENTS: {total_agents} active across {len(org.departments)} departments")
    for dt, dept in org.departments.items():
        print(f"    {dt:12s}: {dept.headcount} agents | "
              f"budget: {dept.budget:10,.0f} C-credits | "
              f"morale: {dept.avg_morale:.2f} | "
              f"efficiency: {dept.efficiency:.3f}")
    
    m = org.metrics
    print(f"\n  FINANCE:")
    print(f"    Credits:       {org.credits:14,.2f} C-credits")
    print(f"    Total Revenue: {org.total_revenue:14,.2f} C-credits")
    print(f"    Burn Rate:     {org.burn_rate:14,.2f} C-credits/tick")
    print(f"    Last Revenue:  {org.revenue:+14,.2f} C-credits")
    
    print(f"\n  ANALYTICS:")
    print(f"    Org Efficiency:      {m.org_efficiency:.3f}")
    print(f"    Innovation Rate:     {m.innovation_rate:.3f}")
    print(f"    Conflict Score:      {m.conflict_score:.3f}")
    print(f"    Market Adaptability: {m.market_adaptability:.3f}")
    print(f"    Capital Efficiency:  {m.capital_efficiency:.3f}")
    
    print(f"\n  MARKET:")
    print(f"    Demand Index:        {org.market.demand_index:.3f}")
    print(f"    Competitor Pressure: {org.market.competitor_pressure:.3f}")
    print(f"    Product-Market Fit:  {org.market.product_market_fit:.3f}")
    print(f"    External Shock:      {org.market.external_shock or 'none'}")
    
    print(f"\n  PERFORMANCE: {org.tick / max(0.001, elapsed):.0f} tick/sec")
    print(f"\n  COGNITIA SIMULATION COMPLETE!")
    print("=" * 72)


def run_simulation(config: dict = None):
    """Run the full simulation."""
    default_config = {
        "seed": 42,
        "initial_credits": 100000.0,
        "total_ticks": 5000,
        "report_interval": 500,
        "mode": "fast",
    }
    config = config or default_config
    config = {**default_config, **config}
    
    print_banner(config)
    
    org = create_organization(config["seed"], config["initial_credits"])
    
    start = time.time()
    
    if config["mode"] == "fast":
        # Fast mode: no prints during simulation
        for i in range(config["total_ticks"]):
            execute_tick(org)
            if (i + 1) % config["report_interval"] == 0:
                elapsed = time.time() - start
                alive = sum(d.headcount for d in org.departments.values())
                print(f"  T{org.tick:5d} | {org.credits:12,.0f} C-credits | "
                      f"eff: {org.metrics.org_efficiency:.3f} | "
                      f"inn: {org.metrics.innovation_rate:.3f} | "
                      f"{org.tick / elapsed:.0f} tick/sec")
    else:
        # Verbose mode
        for i in range(config["total_ticks"]):
            execute_tick(org)
    
    elapsed = time.time() - start
    print_final_report(org, elapsed)
    
    # Save report
    report = {
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "config": config,
        "final_state": {
            "tick": org.tick,
            "credits": org.credits,
            "total_revenue": org.total_revenue,
            "burn_rate": org.burn_rate,
        },
        "analytics": {
            "org_efficiency": org.metrics.org_efficiency,
            "innovation_rate": org.metrics.innovation_rate,
            "conflict_score": org.metrics.conflict_score,
            "market_adaptability": org.metrics.market_adaptability,
            "capital_efficiency": org.metrics.capital_efficiency,
        },
        "performance": {
            "elapsed_seconds": elapsed,
            "ticks_per_second": org.tick / max(0.001, elapsed),
        },
    }
    
    report_path = os.path.join(os.path.dirname(__file__), "..", "report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    return report


def main():
    """Entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cognitia — Corporate Evolution Engine")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--credits", type=float, default=100000.0)
    parser.add_argument("--ticks", type=int, default=5000)
    parser.add_argument("--interval", type=int, default=500)
    parser.add_argument("--mode", choices=["fast", "verbose"], default="fast")
    args = parser.parse_args()
    
    config = {
        "seed": args.seed,
        "initial_credits": args.credits,
        "total_ticks": args.ticks,
        "report_interval": args.interval,
        "mode": args.mode,
    }
    
    run_simulation(config)


if __name__ == "__main__":
    main()
