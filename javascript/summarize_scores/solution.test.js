const { summarizeScores } = require("./solution");
const validFixture = require("./fixtures/valid_reviews.json");
const invalidFixture = require("./fixtures/invalid_reviews.json");

test("groups and averages scores", () => {
  const input = [
    { category: "accuracy", score: 4 },
    { category: "accuracy", score: 5 },
    { category: "safety", score: 3 },
  ];
  expect(summarizeScores(input)).toEqual({
    accuracy: { count: 2, average: 4.5 },
    safety: { count: 1, average: 3 },
  });
});

test("rejects invalid scores", () => {
  expect(() => summarizeScores([{ category: "accuracy", score: 7 }])).toThrow();
});

test("returns an empty object for empty input", () => {
  expect(summarizeScores([])).toEqual({});
});

test.each([null, {}, "reviews", 4])("rejects non-array input", (input) => {
  expect(() => summarizeScores(input)).toThrow(TypeError);
});

test.each([null, [], "review", 3])("rejects malformed review entries", (entry) => {
  expect(() => summarizeScores([entry])).toThrow(TypeError);
});

test.each(["", "   ", null, 4])("rejects invalid categories", (category) => {
  expect(() => summarizeScores([{ category, score: 2 }])).toThrow(TypeError);
});

test("trims and merges normalized categories", () => {
  expect(
    summarizeScores([
      { category: " accuracy ", score: 2 },
      { category: "accuracy", score: 4 },
    ])
  ).toEqual({ accuracy: { count: 2, average: 3 } });
});

test.each([-0.01, 5.01, "3", null, NaN, Infinity, -Infinity])(
  "rejects invalid score values",
  (score) => {
    expect(() => summarizeScores([{ category: "accuracy", score }])).toThrow(TypeError);
  }
);

test("accepts score boundaries", () => {
  expect(
    summarizeScores([
      { category: "low", score: 0 },
      { category: "high", score: 5 },
    ])
  ).toEqual({ high: { count: 1, average: 5 }, low: { count: 1, average: 0 } });
});

test("sorts keys and rounds averages to two decimal places", () => {
  const result = summarizeScores([
    { category: "zeta", score: 1 },
    { category: "alpha", score: 1 },
    { category: "alpha", score: 2 },
    { category: "alpha", score: 2 },
  ]);
  expect(Object.keys(result)).toEqual(["alpha", "zeta"]);
  expect(result.alpha).toEqual({ count: 3, average: 1.67 });
});

test("does not mutate its input", () => {
  const input = [{ category: " accuracy ", score: 4, note: "keep" }];
  const before = JSON.parse(JSON.stringify(input));
  summarizeScores(input);
  expect(input).toEqual(before);
});

test.each([{ score: 2 }, { category: "accuracy" }])(
  "rejects missing required fields",
  (review) => {
    expect(() => summarizeScores([review])).toThrow(TypeError);
  }
);

test("matches the valid fixture", () => {
  expect(summarizeScores(validFixture.input)).toEqual(validFixture.expected);
});

test.each(invalidFixture.cases)("rejects fixture case: $name", ({ input }) => {
  expect(() => summarizeScores(input)).toThrow(TypeError);
});
