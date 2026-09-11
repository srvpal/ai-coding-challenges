# AI Coding Challenges

Original, self-contained coding tasks with precise specifications, reference
implementations, structured fixtures, and deterministic evaluation.

## What This Repository Demonstrates

- Problem statements with explicit input, output, and invalid-input rules
- Reference implementations in Python and JavaScript
- Automated checks for edge cases, failure conditions, and input immutability
- Deterministic fixtures, manifests, and pass/fail evaluation results
- Reproducible dependency installation and continuous integration

## Challenges

| Challenge | Language | What it tests | Evaluator |
| --- | --- | --- | --- |
| [Normalize Event Records](python/normalize_events/README.md) | Python | Schema validation, normalization, sorting, and immutability | pytest |
| [Summarize Review Scores](javascript/summarize_scores/README.md) | JavaScript | Aggregation, normalized categories, rounding, and invalid values | Jest |
| [Resolve Layered Configuration](python/resolve_config/README.md) | Python | Precedence, deletion semantics, protected keys, and defensive copying | pytest |
| [Validate Event State Sequences](python/validate_event_sequence/README.md) | Python | Structured events, chronological ordering, and state transitions | pytest |

## How a Challenge Is Structured

Each challenge contains a README specification, a reference solution, automated
tests, small JSON fixtures, and a machine-readable manifest. Configuration
Resolution also includes one intentionally incomplete baseline. Its tests show
that explicit deletion and protected-key cases distinguish it from the reference
behavior.

## Evaluation

`tools/evaluate.py` discovers the challenge manifests and runs each declared test
command. It emits deterministic JSON with a `pass` or `fail` status for every
challenge and exits nonzero if any evaluator fails. It does not assign scores.

`tools/validate_manifests.py` checks required metadata, unique challenge IDs, and
referenced entry points, working directories, and fixture files.

## Run Locally

Python 3.12 and Node.js 22 match the CI environment.

```bash
python -m pip install -r requirements.txt
cd javascript/summarize_scores
npm ci
cd ../..
python tools/validate_manifests.py
python tools/evaluate.py
```

Run a single evaluator with the command in that challenge's README or manifest.

## Reproducibility

Python's direct test dependency is pinned in `requirements.txt`. JavaScript uses
a generated lockfile and `npm ci`. GitHub Actions runs Python and JavaScript tests
in independent jobs, then runs the shared evaluator in a third clean job.

A Docker image is omitted because this small repository already fixes runtime
versions and dependency installation in CI. A combined Python and Node image
would duplicate that setup and add another mixed-runtime build definition.

## Repository Structure

```text
.github/workflows/tests.yml
javascript/summarize_scores/
  fixtures/
  README.md
  manifest.json
  package.json
  package-lock.json
  solution.js
  solution.test.js
python/
  normalize_events/
    fixtures/ README.md manifest.json solution.py test_solution.py
  resolve_config/
    baselines/incomplete.py
    fixtures/ README.md manifest.json solution.py test_solution.py test_baseline.py
  validate_event_sequence/
    fixtures/ README.md manifest.json solution.py test_solution.py
requirements.txt
tests/
tools/
```
