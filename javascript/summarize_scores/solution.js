"use strict";

function summarizeScores(reviews) {
  if (!Array.isArray(reviews)) {
    throw new TypeError("reviews must be an array");
  }

  const totals = {};

  for (const [index, review] of reviews.entries()) {
    if (!review || typeof review !== "object" || Array.isArray(review)) {
      throw new TypeError(`review ${index} must be an object`);
    }

    const { category, score } = review;
    if (typeof category !== "string" || category.trim() === "") {
      throw new TypeError(`review ${index} has an invalid category`);
    }
    if (typeof score !== "number" || !Number.isFinite(score) || score < 0 || score > 5) {
      throw new TypeError(`review ${index} has an invalid score`);
    }

    const key = category.trim();
    totals[key] ??= { count: 0, total: 0 };
    totals[key].count += 1;
    totals[key].total += score;
  }

  return Object.fromEntries(
    Object.entries(totals)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([category, data]) => [
        category,
        { count: data.count, average: Number((data.total / data.count).toFixed(2)) },
      ])
  );
}

module.exports = { summarizeScores };
