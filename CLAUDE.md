# Project Guidelines

## Project Rules

### ML Best Practices
- **Seeds**: Always use `random_state=42`, `np.random.seed(42)`, `torch.manual_seed(42)`
- **Validation**: 5-fold stratified cross-validation for tabular data
- **Data leakage**: NEVER allow leakage from train to validation/test
- **Reproducibility**: Pin all dependencies in `requirements.txt`

### Code Standards
- **Type hints**: Mandatory for all functions
- **Docstrings**: Google style for public functions
- **Config**: Use YAML/JSON configs instead of hardcoded values
- **Logging**: Use `loguru` for logging, not print()

### Kaggle Competitions
- Check `sample_submission.csv` format before submitting
- Save all experiments in `experiments/` with date and description
- Save OOF predictions for stacking

## Commands

```bash
# Training
python train.py --config configs/baseline.yaml

# Inference  
python inference.py --checkpoint best_model.pt --output submission.csv

# Submit
kaggle competitions submit -c COMPETITION_NAME -f submission.csv -m "description"
```

## Project Structure

```
project/
├── configs/           # YAML configs
├── data/              # Data (do not commit!)
├── experiments/       # Experiment results
├── notebooks/         # EDA and prototypes
├── src/               # Main code
│   ├── data/          # Loading and preprocessing
│   ├── models/        # Model architectures
│   ├── training/      # Training loops
│   └── utils/         # Utilities
└── submissions/       # Submissions
```

## Prohibited

- `rm -rf` without explicit confirmation
- Commits to main without PR
- Hardcoded paths to data
- Training on full data without validation
