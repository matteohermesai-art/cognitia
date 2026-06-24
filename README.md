# Cognitia — Autonomous Corporate Evolution Engine

A multi-agent simulation platform for modeling self-governing corporate entities composed of autonomous AI departments that compete, cooperate, and evolve over time.

## Highlights

- **5 autonomous departments** with distinct decision loops and objectives
- **Persistent agents** with morale, skill, memory, and attrition
- **Internal economy** — C-credits, dynamic budget allocation, ROI tracking
- **External market** — demand fluctuation, competitor pressure, external shocks
- **Analytics engine** — efficiency, innovation, conflict, adaptability metrics
- **Deterministic replay** — seed-based reproducibility
- **High performance** — ~23k ticks/second

## Architecture

```
                   REST API (FastAPI)
                        |
            +-----------+-----------+
            |                       |
      CEO Decision Loop     Market Simulator
            |                       |
    +-------+-------+       +------+------+
    |       |       |       |             |
  Finance   R&D   Marketing    HR     External
  Dept      Dept    Dept      Dept    Market
    |       |       |         |
  Agents  Agents  Agents   Agents
```

### Departments

| Department | Role | Key Metric |
|------------|------|------------|
| **Executive** | Strategy, budget allocation, conflict resolution | Org Efficiency |
| **Finance** | Capital management, cashflow prediction | Burn Rate |
| **R&D** | Product innovation, experiments | Innovation Score |
| **Marketing** | Demand generation, perception management | Market Adaptability |
| **HR** | Hiring/firing, morale, team structure | Attrition Rate |

### Agent Model

Each agent has:
- **Persistent state**: morale, skill, salary, level, age
- **Memory buffer**: last 20 actions + outcomes
- **Role-specific decision function** per tick
- **Utility function** aligned to departmental goals
- **Communication** with other departments

### Economy

| Metric | Description |
|--------|-------------|
| **C-credits** | Single corporate currency |
| **Budget** | Dynamic per-tick allocation by CEO |
| **Revenue** | Marketing efficiency × demand + R&D innovation bonus |
| **Burn Rate** | Sum of all department salaries |
| **ROI** | Revenue per department |

### Market Simulation

| Factor | Behavior |
|--------|----------|
| **Demand** | Random walk, influenced by Marketing |
| **Competition** | Random walk, countered by Marketing |
| **Product-Market Fit** | Improved by R&D innovation |
| **External Shocks** | Random: regulation, breakthrough, crash, opportunity |

### Analytics (per tick)

| Metric | Formula |
|--------|---------|
| **Org Efficiency** | Average of department efficiencies |
| **Innovation Rate** | R&D department innovation score |
| **Conflict Score** | Average of department conflict indices |
| **Market Adaptability** | (demand + (1 - competition)) / 2 |
| **Capital Allocation** | Total budget / total credits |

## Quick Start

```bash
git clone https://github.com/matteohermesai-art/cognitia.git
cd cognitia

# Run simulation
python src/main.py

# With custom config
SEED=123 TOTAL_TICKS=10000 python src/main.py
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SEED` | `42` | Random seed for reproducibility |
| `INITIAL_CREDITS` | `100000` | Starting capital (C-credits) |
| `TOTAL_TICKS` | `5000` | Simulation length |
| `REPORT_INTERVAL` | `500` | Ticks between progress reports |

## API (Planned)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/org/start` | Start simulation |
| `POST` | `/org/run?steps=N` | Run N ticks |
| `GET` | `/org/state` | Current organization state |
| `GET` | `/org/department/{id}` | Department details |
| `GET` | `/org/metrics` | Analytics metrics |
| `GET` | `/org/market` | Market state |

## Tech Stack

- **Python 3.11+** with AsyncIO
- **FastAPI** (planned for v1.1)
- **SQLAlchemy + PostgreSQL** (planned for v1.1)
- **structlog** for structured logging
- **Docker** containerization

## Project Structure

```
cognitia/
├── src/                   # Source code
│   ├── core_engine/       # Tick engine, state management
│   ├── agents/            # Agent base + specialized roles
│   ├── departments/       # Department decision logic
│   ├── economy/           # Budget, revenue, market
│   ├── market/            # External market simulation
│   ├── persistence/       # State storage (planned)
│   ├── api/               # FastAPI endpoints (planned)
│   ├── worker/            # Background tick loop (planned)
│   └── analytics/         # Metrics computation
├── tests/                 # Test suite
├── scripts/               # Utility scripts
├── docker-compose.yml     # Container orchestration
├── Dockerfile             # Multi-stage build
├── pyproject.toml         # Project configuration
├── requirements.txt       # Dependencies
├── .env.example           # Environment template
├── README.md              # This file
├── CHANGELOG.md           # Version history
├── CONTRIBUTING.md        # Contribution guidelines
├── DECISIONS.md           # Architecture Decision Records
└── LICENSE                # MIT License
```

## Performance

| Metric | Value |
|--------|-------|
| Tick rate | ~23,000/sec |
| Memory | ~200MB |
| Agents | Unlimited |
| Deterministic | Yes (with fixed seed) |

## Roadmap

- [ ] REST API with FastAPI
- [ ] PostgreSQL persistence layer
- [ ] WebSocket real-time updates
- [ ] Multi-organization support
- [ ] Visualization dashboard
- [ ] Plugin system for custom departments
- [ ] Machine learning for agent decisions

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Acknowledgments

Inspired by multi-agent simulation, organizational theory, and cyberpunk fiction.
