---
description: Project development workflow - structured task management
---

## Project Workflow

### 1. Define Scope
Clearly define what this project should accomplish:
```
GOAL: [One sentence description]
SUCCESS CRITERIA:
- Criterion 1
- Criterion 2
- Criterion 3
```

### 2. Break Down Tasks
Create hierarchical task structure:
```markdown
## Phase 1: Foundation
- [ ] Task 1.1
- [ ] Task 1.2

## Phase 2: Core Features
- [ ] Task 2.1
- [ ] Task 2.2

## Phase 3: Polish
- [ ] Task 3.1
- [ ] Task 3.2
```

### 3. Setup Repository
```bash
mkdir -p src tests docs configs
touch README.md requirements.txt .env.example
git init
```

### 4. Implement with Tests
For each feature:
1. Write test first (if applicable)
2. Implement feature
3. Verify test passes
4. Document

### 5. Code Quality Checks
```bash
# Linting
ruff check src/

# Type checking
mypy src/

# Tests
pytest tests/ -v
```

### 6. Documentation
- README with setup and usage
- Docstrings for public APIs
- Architecture decisions in docs/

### 7. Review Checklist
Before marking complete:
- [ ] All tests pass
- [ ] No hardcoded secrets
- [ ] README is complete
- [ ] Dependencies pinned
- [ ] Works on clean install
