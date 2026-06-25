"""Market module: external market simulation with demand, competition, shocks."""
from dataclasses import dataclass, field
from typing import Optional
import random


@dataclass
class MarketState:
    """External market conditions."""
    demand_index: float = 0.5
    competitor_pressure: float = 0.3
    product_market_fit: float = 0.4
    external_shock: Optional[str] = None
    shock_remaining: int = 0
    shock_history: list = field(default_factory=list)

    def update(self) -> None:
        """Update market conditions for one tick."""
        self.demand_index = max(0.0, min(1.0, self.demand_index + random.uniform(-0.05, 0.05)))
        self.competitor_pressure = max(0.0, min(1.0, self.competitor_pressure + random.uniform(-0.03, 0.03)))
        if random.random() < 0.02 and not self.external_shock:
            self.external_shock = random.choice(["regulation", "breakthrough", "crash", "opportunity"])
            self.shock_remaining = random.randint(10, 30)
            self.shock_history.append({
                "type": self.external_shock,
                "duration": self.shock_remaining,
            })
        if self.shock_remaining > 0:
            self.shock_remaining -= 1
        else:
            self.external_shock = None

    def summary(self) -> dict:
        return {
            "demand_index": round(self.demand_index, 3),
            "competitor_pressure": round(self.competitor_pressure, 3),
            "product_market_fit": round(self.product_market_fit, 3),
            "external_shock": self.external_shock,
            "shock_remaining": self.shock_remaining,
            "total_shocks": len(self.shock_history),
        }
