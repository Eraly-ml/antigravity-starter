# Antigravity ML Starter Kit

A collection of workflows, hooks, and agents for ML/Kaggle development with Antigravity.

## Quick Start

1. Clone this repo or copy the `.agent` folder to your project root
2. Copy `CLAUDE.md` to your project root and customize it
3. Use workflows with slash commands: `/kaggle-submit`, `/train-model`, `/eda`

## Structure

```
your-project/
├── CLAUDE.md                    # Project guidelines (customize this)
└── .agent/
    ├── workflows/               # Slash commands
    │   ├── kaggle-submit.md     # /kaggle-submit
    │   ├── train-model.md       # /train-model
    │   └── eda.md               # /eda
    ├── hooks/                   # Command validators
    │   └── command_validator.py # Blocks dangerous commands
    └── agents/                  # Specialized agents
        ├── kaggle-analyst.md    # @kaggle-analyst
        └── ml-code-reviewer.md  # @ml-code-reviewer
```

## Workflows

### /kaggle-submit
Validates and submits to Kaggle competitions:
- Checks submission format
- Validates for duplicate IDs
- Submits and checks leaderboard

### /train-model
ML training workflow:
- GPU availability check
- Config validation
- Training with monitoring

### /eda
Comprehensive EDA workflow:
- Data loading and info
- Missing values analysis
- Distribution plots
- Correlation heatmaps

## Agents

### @kaggle-analyst
Analyzes Kaggle competitions:
- Reviews top solutions
- Identifies winning patterns
- Suggests feature engineering

### @ml-code-reviewer
Reviews ML code for:
- Data leakage
- Reproducibility issues
- Best practices compliance

## Hooks

### command_validator.py
Blocks dangerous commands like:
- `rm -rf /`
- Fork bombs
- Direct disk writes

Warns about:
- Force pushes
- Insecure permissions

## Customization

Edit `CLAUDE.md` to add your project-specific rules:
- Coding standards
- ML best practices
- Project structure
- Prohibited actions

## License

MIT
