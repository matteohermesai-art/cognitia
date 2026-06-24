# Contributing to Cognitia

Welcome! Thank you for your interest in contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the project

## How to Contribute

```bash
git clone https://github.com/matteohermesai-art/cognitia.git
cd cognitia

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python src/main.py  # Run simulation
pytest tests/        # Run tests
```

## Commit Convention

Follow conventional commits:
```
feat: add new department type
fix: resolve budget allocation bug
docs: update API documentation
refactor: extract market logic into module
test: add integration tests for HR department
```

## Pull Request Process

1. Fork, branch, implement
2. Ensure simulation runs successfully
3. Update CHANGELOG.md
4. Submit PR with clear description

## Areas for Contribution

- New department types (Operations, Legal, Support)
- Machine learning for agent decisions
- Visualization dashboard
- Performance optimization
- API implementation
- Persistence layer

## Questions?

Open an issue or contact matteohermesai@gmail.com.
