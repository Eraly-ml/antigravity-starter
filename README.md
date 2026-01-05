# Antigravity Starter Kit

A collection of workflows, hooks, and agents for ML/Kaggle development with Antigravity.

## Quick Start

1. Clone this repo or copy the `.agent` folder to your project root
2. Copy `CLAUDE.md` to your project root and customize it
3. Use workflows with slash commands

## Structure

```
your-project/
├── CLAUDE.md                        # Project guidelines (customize this)
└── .agent/
    ├── workflows/                   # Slash commands
    │   ├── kaggle-submit.md         # /kaggle-submit
    │   ├── train-model.md           # /train-model
    │   ├── eda.md                   # /eda
    │   ├── hackathon.md             # /hackathon
    │   ├── project.md               # /project
    │   └── research.md              # /research
    ├── hooks/                       # Command validators
    │   └── command_validator.py     # Blocks dangerous commands
    └── agents/                      # Specialized agents
        ├── kaggle-analyst.md        # @kaggle-analyst
        ├── ml-code-reviewer.md      # @ml-code-reviewer
        ├── hackathon-assistant.md   # @hackathon-assistant
        ├── project-manager.md       # @project-manager
        └── research-assistant.md    # @research-assistant
```

## Workflows

### ML Workflows

| Command | Description |
|---------|-------------|
| `/kaggle-submit` | Validate and submit to Kaggle |
| `/train-model` | Train model with GPU monitoring |
| `/eda` | Create comprehensive EDA |

### Project Type Workflows

| Command | Description |
|---------|-------------|
| `/hackathon` | Fast prototyping, requirement tracking, deadline focus |
| `/project` | Structured task management, quality checks |
| `/research` | Experiment tracking, paper review, ablation studies |

## Agents

### ML Agents

| Agent | Description |
|-------|-------------|
| `@kaggle-analyst` | Analyzes competitions, reviews winning solutions |
| `@ml-code-reviewer` | Reviews for data leakage, best practices |

### Project Agents

| Agent | Description |
|-------|-------------|
| `@hackathon-assistant` | Fast prototyping, ships MVPs quickly |
| `@project-manager` | Task tracking, quality gates, structured development |
| `@research-assistant` | Experiment tracking, paper review, ablations |

## Hooks

### command_validator.py

Blocks dangerous commands:
- `rm -rf /` - destructive deletion
- Fork bombs
- Direct disk writes

Warns about:
- Force pushes
- Insecure permissions

## Usage Examples

### Hackathon
```
/hackathon
[Paste your task specification]
```
The agent will parse requirements, create MVP plan, and track progress.

### Research Project
```
/research
[Describe your research question]
```
Sets up experiment tracking, literature review template, and result logging.

### Kaggle Competition
```
/kaggle-submit
```
Validates submission format and pushes to leaderboard.

## Customization

Edit `CLAUDE.md` for project-specific rules:
- Coding standards
- ML best practices
- Project structure
- Prohibited actions

## License

MIT
