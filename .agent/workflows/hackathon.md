---
description: Hackathon development workflow - follow technical requirements precisely
---

## Hackathon Workflow

### 1. Parse Technical Requirements
Read and extract all requirements from the task specification:
```
- Mandatory features (MUST have)
- Optional features (bonus points)
- Technical constraints (languages, frameworks, APIs)
- Submission format and deadline
- Evaluation criteria
```

### 2. Create Implementation Plan
Based on requirements, create a prioritized task list:
```markdown
## MVP (Minimum Viable Product) - First 50% of time
- [ ] Core feature 1
- [ ] Core feature 2
- [ ] Basic UI/demo

## Polish - Next 30% of time
- [ ] Error handling
- [ ] Edge cases
- [ ] UI improvements

## Bonus Features - Remaining 20%
- [ ] Optional feature 1
- [ ] Optional feature 2
```

### 3. Setup Project
```bash
mkdir -p src tests docs
touch README.md requirements.txt
```

### 4. Implement MVP First
Focus on working demo, not perfect code. Ship fast.

### 5. Test Against Requirements
Before submission, verify EVERY requirement:
```
- [ ] Requirement 1: DONE/NOT DONE
- [ ] Requirement 2: DONE/NOT DONE
- [ ] Submission format correct
- [ ] Demo works end-to-end
```

### 6. Prepare Submission
- Clean README with setup instructions
- Demo video/screenshots if required
- All files in correct format
