---
description: Kaggle competition submission workflow
---
// turbo

## Kaggle Submit Workflow

### 1. Validate submission format
Check submission.csv format:
```bash
python -c "import pandas as pd; df=pd.read_csv('submission.csv'); print(f'Shape: {df.shape}'); print(df.head())"
```

### 2. Check for duplicate IDs
```bash
python -c "import pandas as pd; df=pd.read_csv('submission.csv'); print(f'Duplicates: {df.iloc[:,0].duplicated().sum()}')"
```

### 3. Submit
```bash
kaggle competitions submit -c COMPETITION_NAME -f submission.csv -m "DESCRIPTION"
```

### 4. Check status
Wait 30 seconds and check:
```bash
kaggle competitions submissions -c COMPETITION_NAME | head -5
```
