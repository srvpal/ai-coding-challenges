# Summarize Review Scores

## Problem

Implement `summarizeScores(reviews)` to validate review records and summarize scores by normalized category without changing the input.

## Input

`reviews` must be an array of objects. Every object must contain:

- `category`: a non-empty string after trimming whitespace
- `score`: a finite number from `0` to `5`, inclusive

Additional fields are accepted and ignored.

## Output

Return an object whose keys are trimmed category names in lexicographic order. Each value contains:

```javascript
{ count: number, average: number }
```

## Rules

- Trim surrounding whitespace from each category.
- Merge categories that become identical after trimming.
- Sort category keys lexicographically.
- Round each average to two decimal places and return it as a number.
- Return an empty object for empty input.
- Do not mutate the input.

## Invalid Input

Throw `TypeError` when the input is not an array, an entry is not an object, a category is missing, blank, or not a string, or a score is missing, non-numeric, non-finite, or outside `0` through `5`.

## Examples

```javascript
summarizeScores([
  { category: " accuracy ", score: 4 },
  { category: "accuracy", score: 5 },
  { category: "safety", score: 3 },
]);
```

returns:

```javascript
{
  accuracy: { count: 2, average: 4.5 },
  safety: { count: 1, average: 3 },
}
```

## Evaluation Criteria

The tests check grouping, category normalization, deterministic ordering, two-decimal rounding, empty input, score boundaries, malformed records, missing fields, non-finite scores, and input immutability.

## Run Locally

From the repository root:

```bash
npm ci --prefix javascript/summarize_scores
npm test --prefix javascript/summarize_scores
```
