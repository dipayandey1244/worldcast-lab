# Contributing

Thanks for your interest in WORLDCAST.

## Development setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest
```

## Research contributions
- Keep experiments reproducible: record seeds, versions, configuration and compute.
- Use chronological splits for forecasting.
- Distinguish synthetic simulator results from real-world evidence.
- Include a baseline and uncertainty analysis when proposing a model improvement.
- Document interventions and evaluate policies on matched initial conditions.

Please open an issue before large architectural changes.
