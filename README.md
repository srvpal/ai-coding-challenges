# AI Coding Challenges

Original, self-contained coding exercises that demonstrate benchmark design, precise requirements, reference implementations, and automated testing.

## Challenges

### Python: Normalize Event Records

Normalize inconsistent event dictionaries into a deterministic schema while validating required fields.

### JavaScript: Summarize Review Scores

Aggregate reviewer scores by category without mutating the input.

## Repository structure

```text
python/normalize_events/
  README.md
  solution.py
  test_solution.py
javascript/summarize_scores/
  README.md
  solution.js
  solution.test.js
.github/workflows/tests.yml
```

## Run Python tests

```bash
python -m pip install pytest
pytest
```

## Run JavaScript tests

```bash
cd javascript/summarize_scores
npm install
npm test
```

## Design principles

- Unambiguous task statements
- Deterministic expected behavior
- Edge-case coverage
- Clear failure messages
- Original examples without proprietary material
