---
description: Create comprehensive EDA notebook
---

## EDA Workflow

### 1. Create structure
```bash
mkdir -p notebooks figures
```

### 2. Load data and check
```python
import pandas as pd
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')
print(f"Train: {train.shape}, Test: {test.shape}")
print(train.info())
```

### 3. Missing values
```python
missing = train.isnull().sum()
missing[missing > 0].sort_values(ascending=False)
```

### 4. Target distribution
```python
import matplotlib.pyplot as plt
train['target'].value_counts().plot(kind='bar')
plt.savefig('figures/target_dist.png')
```

### 5. Numeric features
```python
train.describe()
train.hist(figsize=(15, 10))
plt.savefig('figures/numeric_dist.png')
```

### 6. Correlations
```python
import seaborn as sns
corr = train.select_dtypes('number').corr()
sns.heatmap(corr, cmap='coolwarm')
plt.savefig('figures/correlation.png')
```

### 7. Train vs Test distribution
Check that distributions match between train and test.
