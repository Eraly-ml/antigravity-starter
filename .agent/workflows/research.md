---
description: Research workflow - experiment tracking and paper review
---

## Research Workflow

### 1. Define Research Question
```
RESEARCH QUESTION: [Clear, specific question]
HYPOTHESIS: [What you expect to find]
METRICS: [How you will measure success]
```

### 2. Literature Review
Search and document related work:
```markdown
## Related Papers
| Paper | Year | Key Finding | Relevance |
|-------|------|-------------|-----------|
| [Link] | 2024 | Finding | High/Med/Low |
```

### 3. Setup Experiment Tracking
```bash
# Create experiment directory
mkdir -p experiments/$(date +%Y%m%d)_experiment_name

# Initialize tracking
mlflow ui --port 5000 &
# or
wandb init
```

### 4. Experiment Structure
```
experiments/
└── YYYYMMDD_experiment_name/
    ├── config.yaml          # Hyperparameters
    ├── logs/                 # Training logs
    ├── checkpoints/          # Model weights
    ├── results/              # Metrics, plots
    └── notes.md              # Observations
```

### 5. Run Experiment
Log everything:
```python
# Log config
mlflow.log_params(config)

# Log metrics
mlflow.log_metric("accuracy", acc)

# Log artifacts
mlflow.log_artifact("model.pt")
```

### 6. Document Results
After each experiment, update notes:
```markdown
## Experiment: [Name]
Date: YYYY-MM-DD
Config: [key params]

### Results
- Metric 1: X.XX
- Metric 2: Y.YY

### Observations
- What worked
- What didn't
- Next steps
```

### 7. Ablation Studies
Systematically test components:
```markdown
| Component | Baseline | With Component | Delta |
|-----------|----------|----------------|-------|
| Feature A | 0.85     | 0.87           | +0.02 |
```

### 8. Write Report
Structure:
1. Abstract
2. Introduction / Motivation
3. Related Work
4. Method
5. Experiments
6. Results
7. Conclusion
