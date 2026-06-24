# Cognitia — Autonomous Corporate Evolution Engine

A multi-agent simulation platform for modeling self-governing corporate entities composed of autonomous AI departments.

## Highlights

- **5 autonomous departments**: Executive, Finance, R&D, Marketing, HR
- **Persistent agents** with morale, skill, memory, and attrition
- **Internal economy**: C-credits, budget allocation, ROI tracking
- **External market simulation**: demand, competition, external shocks
- **Analytics engine**: efficiency, innovation, conflict, adaptability metrics
- **Deterministic replay**: seed-based reproducibility
- **Fast**: ~23k ticks/second

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

## Departments

| Department | Role | Key Metric |
|------------|------|------------|
| **Executive** | Strategy, budget allocation, conflict resolution | Org Efficiency |
| **Finance** | Capital management, cashflow prediction | Burn Rate |
| **R&D** | Product innovation, experiments | Innovation Score |
| **Marketing** | Demand generation, perception management | Market Adaptability |
| **HR** | Hiring/firing, morale, team structure | Attrition Rate |

## Quick Start

```bash
git clone https://github.com/matteohermesai-art/cognitia.git
cd cognitia
pip install -r requirements.txt
python src/main.py
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
| `GET` | `/org/state` | Current state |
| `GET` | `/org/department/{id}` | Department details |
| `GET` | `/org/metrics` | Analytics |
| `GET` | `/org/market` | Market state |

## Tech Stack

- Python 3.11+ with AsyncIO
- FastAPI (planned)
- SQLAlchemy + PostgreSQL (planned)
- structlog for structured logging
- Docker containerization

## Project Structure

```
cognitia/
├── src/                   # Source code
│   ├── core_engine/       # Tick engine, state management
│   ├── agents/            # Agent implementations
│   ├── departments/       # Department logic
│   ├── economy/           # Budget, revenue, market
│   ├── market/            # External market simulation
│   ├── persistence/       # State storage
│   ├── api/               # FastAPI endpoints
│   ├── worker/            # Background tick loop
│   └── analytics/         # Metrics computation
├── tests/                 # Test suite
├── scripts/               # Utilities
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── DECISIONS.md
```

## Performance

| Metric | Value |
|--------|-------|
| Tick rate | ~23,000/sec |
| Memory | ~200MB |
| Agents supported | Unlimited |
| Persistence | PostgreSQL |

## Roadmap

- [ ] REST API with FastAPI
- [ ] PostgreSQL persistence layer
- [ ] WebSocket real-time updates
- [ ] Multi-organization support
- [ ] Visualization dashboard
- [ ] Plugin system for custom departments

## License

MIT License — see [LICENSE](LICENSE)
