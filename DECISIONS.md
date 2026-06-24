# Architecture Decision Records (ADR)

## ADR-001: Python with Dataclasses for Agent Model

**Date**: 2025-06-24
**Status**: Accepted
**Context**: Need lightweight, fast agent representation. Full SQLAlchemy overhead not needed for v1.0.

**Decision**: Use Python dataclasses with enums for agent state. Defer SQLAlchemy to persistence layer (v1.1).

**Consequences**:
- Fast execution (~23k ticks/sec)
- Simple serialization
- Migration to ORM later requires data migration script

---

## ADR-002: Single Script for v1.0

**Date**: 2025-06-24
**Status**: Accepted
**Context**: Need to deliver working simulation quickly. Full modular structure adds complexity.

**Decision**: Single `src/main.py` script with inline logic. Restructure into modules when adding API layer.

**Consequences**:
- Faster time to demo
- Refactoring needed for v1.1
- Acceptable for proof-of-concept

---

## ADR-003: Deterministic Simulation via Seed

**Date**: 2025-06-24
**Status**: Accepted
**Context**: Must support reproducible results for testing and debugging.

**Decision**: Use `random.seed()` at startup. All randomness flows through Python `random` module.

**Consequences**:
- Same seed = identical results
- Cannot use system entropy sources
- AsyncIO does not affect determinism (single-threaded)

---

## ADR-004: C-credits as Single Currency

**Date**: 2025-06-24
**Status**: Accepted
**Context**: Simplify economy model. Multiple currencies add complexity without clear benefit.

**Decision**: Single corporate currency (C-credits). All departments share the same pool.

**Consequences**:
- Simpler budget allocation
- Clear ROI tracking
- Inter-department competition for resources

---

## ADR-005: Departments as Autonomous Decision Loops

**Date**: 2025-06-24
**Status**: Accepted
**Context**: Each department should have independent behavior, not controlled by a central orchestrator.

**Decision**: Each department has its own decision function called per tick. CEO allocates budgets and resolves conflicts.

**Consequences**:
- Emergent behavior from local decisions
- Conflict generation between departments
- More realistic organizational dynamics
