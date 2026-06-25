"""
Organization state: the central data structure holding all simulation state.
"""
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..agents.models import Agent
    from ..market.models import MarketState  # noqa: F401


@dataclass
class TickMetrics:
    """Metrics computed per tick."""
    org_efficiency: float = 0.5
    innovation_rate: float = 0.0
    conflict_score: float = 0.0
    market_adaptability: float = 0.5
    capital_efficiency: float = 0.5


@dataclass
class OrganizationState:
    """Complete state of the simulated organization."""
    tick: int = 0
    credits: float = 100000.0
    revenue: float = 0.0
    total_revenue: float = 0.0
    burn_rate: float = 0.0
    departments: dict = field(default_factory=dict)
    market: Optional['MarketState'] = None
    metrics: TickMetrics = field(default_factory=TickMetrics)
    decision_log: list = field(default_factory=list)
    tick_history: list = field(default_factory=list)
    running: bool = True

    def snapshot(self) -> dict:
        """Create a serializable snapshot for replay."""
        return {
            "tick": self.tick,
            "credits": self.credits,
            "revenue": self.revenue,
            "total_revenue": self.total_revenue,
            "burn_rate": self.burn_rate,
            "metrics": {
                "org_efficiency": self.metrics.org_efficiency,
                "innovation_rate": self.metrics.innovation_rate,
                "conflict_score": self.metrics.conflict_score,
                "market_adaptability": self.metrics.market_adaptability,
                "capital_efficiency": self.metrics.capital_efficiency,
            },
            "market": {
                "demand_index": self.market.demand_index if self.market else 0.5,
                "competitor_pressure": self.market.competitor_pressure if self.market else 0.3,
                "product_market_fit": self.market.product_market_fit if self.market else 0.4,
                "external_shock": self.market.external_shock if self.market else None,
                "shock_remaining": self.market.shock_remaining if self.market else 0,
            },
            "departments": {
                k: {
                    "budget": d.budget,
                    "efficiency": d.efficiency,
                    "innovation_score": d.innovation_score,
                    "conflict_index": d.conflict_index,
                    "headcount": d.headcount,
                    "avg_morale": d.avg_morale,
                    "burn_rate": d.burn_rate,
                }
                for k, d in self.departments.items()
            },
        }

    def record_tick(self):
        """Save current state to history."""
        self.tick_history.append(self.snapshot())
        if len(self.tick_history) > 1000:
            self.tick_history = self.tick_history[-1000:]
