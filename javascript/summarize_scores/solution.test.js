const { summarizeScores } = require("./solution");

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
