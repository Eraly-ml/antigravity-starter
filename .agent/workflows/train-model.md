---
description: Train ML model with GPU monitoring
---

## Model Training Workflow

### 1. Check GPU
```bash
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
```

### 2. Verify config
Make sure config exists and is valid:
```bash
cat configs/train_config.yaml
```

### 3. Start training
```bash
python train.py --config configs/train_config.yaml
```

### 4. Monitor during training
In a separate terminal:
```bash
watch -n 5 nvidia-smi
```

### 5. After training
- Check logs in `experiments/`
- Save best checkpoint
- Record metrics in README
