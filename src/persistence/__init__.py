"""Persistence layer: SQLAlchemy models and database initialization."""
import asyncio
import os
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON, Enum as SAEnum
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime  # noqa: reused below


class Base(DeclarativeBase):
    pass


class OrgModel(Base):
    """Organization state snapshot per tick."""
    __tablename__ = "organizations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), default="Cognitia Corp")
    tick: Mapped[int] = mapped_column(Integer, nullable=False)
    credits: Mapped[float] = mapped_column(Float, default=100000.0)
    revenue: Mapped[float] = mapped_column(Float, default=0.0)
    total_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    burn_rate: Mapped[float] = mapped_column(Float, default=0.0)
    org_efficiency: Mapped[float] = mapped_column(Float, default=0.5)
    innovation_rate: Mapped[float] = mapped_column(Float, default=0.0)
    conflict_score: Mapped[float] = mapped_column(Float, default=0.0)
    market_adaptability: Mapped[float] = mapped_column(Float, default=0.5)
    demand_index: Mapped[float] = mapped_column(Float, default=0.5)
    competitor_pressure: Mapped[float] = mapped_column(Float, default=0.3)
    product_market_fit: Mapped[float] = mapped_column(Float, default=0.4)
    external_shock: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DeptModel(Base):
    """Department state per tick."""
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    org_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"))
    dept_type: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(128))
    budget: Mapped[float] = mapped_column(Float, default=10000.0)
    efficiency: Mapped[float] = mapped_column(Float, default=0.5)
    innovation_score: Mapped[float] = mapped_column(Float, default=0.0)
    conflict_index: Mapped[float] = mapped_column(Float, default=0.0)
    headcount: Mapped[int] = mapped_column(Integer, default=0)
    avg_morale: Mapped[float] = mapped_column(Float, default=0.0)
    burn_rate: Mapped[float] = mapped_column(Float, default=0.0)
    avg_skill: Mapped[float] = mapped_column(Float, default=0.0)

    org: Mapped["OrgModel"] = relationship(back_populates="departments")


OrgModel.departments = relationship(back_populates="org")


class AgentModel(Base):
    """Agent state per tick."""
    __tablename__ = "agents"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    org_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"))
    name: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(String(32))
    department: Mapped[str] = mapped_column(String(32))
    level: Mapped[int] = mapped_column(Integer, default=1)
    morale: Mapped[float] = mapped_column(Float, default=0.8)
    skill: Mapped[float] = mapped_column(Float, default=0.5)
    salary: Mapped[float] = mapped_column(Float, default=100.0)
    alive: Mapped[bool] = mapped_column(Boolean, default=True)
    age: Mapped[int] = mapped_column(Integer, default=0)
    actions_completed: Mapped[int] = mapped_column(Integer, default=0)
    avg_outcome: Mapped[float] = mapped_column(Float, default=0.0)

    org: Mapped["OrgModel"] = relationship(back_populates="agents")


OrgModel.agents = relationship(back_populates="org")


class DecisionLog(Base):
    """Log of decisions made by departments."""
    __tablename__ = "decision_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    org_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"))
    tick: Mapped[int] = mapped_column(Integer)
    department: Mapped[str] = mapped_column(String(32))
    action: Mapped[str] = mapped_column(String(64))
    details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MarketModel(Base):
    """Market state history."""
    __tablename__ = "market_state"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    org_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"))
    tick: Mapped[int] = mapped_column(Integer)
    demand_index: Mapped[float] = mapped_column(Float)
    competitor_pressure: Mapped[float] = mapped_column(Float)
    product_market_fit: Mapped[float] = mapped_column(Float)
    external_shock: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    shock_remaining: Mapped[int] = mapped_column(Integer, default=0)


class TickHistory(Base):
    """Complete tick history for replay."""
    __tablename__ = "tick_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    org_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"))
    tick: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# Fix relationships
OrgModel.decisions = relationship(back_populates="org")
OrgModel.market_states = relationship(back_populates="org")
OrgModel.tick_history = relationship(back_populates="org")

DecisionLog.org = relationship("OrgModel", back_populates="decisions")
MarketModel.org = relationship("OrgModel", back_populates="market_states")
TickHistory.org = relationship("OrgModel", back_populates="tick_history")


def get_database_url() -> str:
    return os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///cognitia.db"
    )


async def init_database(url: str = None):
    """Create all tables if they don't exist."""
    from sqlalchemy.ext.asyncio import create_async_engine
    db_url = url or get_database_url()
    engine = create_async_engine(db_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    return True
