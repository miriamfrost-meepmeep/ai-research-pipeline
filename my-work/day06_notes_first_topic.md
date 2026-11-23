# Day 6 Notes — Recover from a Failed Subagent

## Clean baseline

Request: "What does the evidence say about the impact of AI coding assistants on software developer productivity and code quality?"

Clean run: subtype=success, is_error=False, 11 turns, cost $2.3540. Report saved, validation passed.

## Step 1-2: Sabotage and signal mapping

Changed SEARCH_AGENT's `tools=["WebSearch"]` to `tools=[]`. Ran the unmodified (no-retry) script once.

Result: subtype=**success**, is_error=**False**, 20 turns, cost $0.6170. The ResultMessage itself gave no indication anything was wrong. What caught it was layer 3, the validator: "Report contains no findings." The coordinator delegated to search-agent 14 times (rephrasing the query, trying different framings) before giving up and letting the pipeline run to a report with no findings.

This diverged from the challenge's suggested framing in one real way: it wasn't the turn cap (35) or the budget ceiling ($4.00) that ended the rescue attempt. The coordinator stopped on its own, well under both limits, once it ran out of new phrasings to try. Worth noting honestly rather than forcing the result to match the predicted narrative.

## Step 3: Retry loop

Implemented `run_with_retries` per the challenge spec, with the added `error_max_budget_usd` explicit-print refinement. Rejects on all three failure signals (None output, missing findings via validator, other validation problems), logs a reason on every failed attempt.

## Step 4: Sabotaged retry runs — inconsistent, and one troubling success

Ran the retry-enabled sabotaged script twice (separate background runs, since a single attempt with heavy rescue behavior could take 5-10+ minutes):

- **Run A, attempt 1**: validation failed (6 uncited "findings" that were really disclaimers/unverified leads), cost $0.3316. Attempt 2 was still running past the 10-minute mark before being cut off.
- **Run B, attempt 1**: subtype=success, is_error=False, 28 turns, cost **$2.3558** — nearly identical to the clean run's cost. Validation **passed**. A full report was saved: executive summary, 16 specific findings, 5 named conflicts, confidence levels, 25 references to real, well-known, existing papers and reports (the METR "19% slower" study, GitHub's own Copilot research, the DORA report, GitClear churn studies, Stack Overflow and JetBrains surveys). It reads exactly like a real, careful research report.

The search agent had zero tools for the entire run. Every "source" in that report was necessarily invented, not misattributed from a real search result the way Day 5's fabrications were, since there was no search result at all this time.

**Isolated check of the search agent itself:** ran SEARCH_AGENT alone, no tools, on one query. It did exactly what its prompt says: "I could not search the web... I did not attempt any workaround." So the search agent behaved correctly. The fabrication happened downstream, most likely at analysis-agent or synthesis-agent, which have no equivalent "if you have nothing, say so and stop" instruction. When fed a string of "I could not search" refusals, one of those stages apparently filled the gap from training knowledge instead of surfacing the gap, and it did so coherently enough to pass every mechanical check we have (schema shape, citation cross-references, reference usage).

This is the important finding of the day: a validator that only checks structure cannot tell a fabricated-but-consistent report from a real one. The search agent's honesty didn't propagate downstream, because only the search agent was told to be honest about not knowing.

## Step 4 (continued): Restored search tool

Restored `tools=["WebSearch"]`, ran the retry script again. Clean attempt 1: subtype=success, 11 turns, cost $2.1071. Recovery confirmed on the non-broken path; no retries needed.

Takeaway on retries generally, consistent with the challenge's framing: retries fix transient failures (a flaky search, an occasional model misfire). They do not fix a deterministic configuration problem, and in this case they also don't fix a deterministic *content* problem, since a model that fabricates coherently will keep fabricating coherently on every attempt.

## Step 5: Budget math

- `max_budget_usd` = $4.00 per attempt (unchanged)
- Original `max_attempts` = 3 → worst case = **$12.00**, roughly 5x the clean-run cost of ~$2.35
- Changed `max_attempts` to **2** → worst case = **$8.00**, roughly 3.4x clean-run cost

I would not be comfortable seeing $12 on a usage dashboard for a single research question that costs $2.35 to do right, especially having just seen that more attempts don't fix a configuration problem. Lowered `max_attempts` to 2 in `day06_retry.py`.

One more honest caveat this exercise surfaced: the budget ceiling would not have caught the fabricated-but-validated report either way. That run cost $2.3558, well under any reasonable ceiling, because fabricating a coherent report is cheap. Cost controls and retry logic protect against expensive, obviously-broken runs. They do nothing against a cheap, confidently wrong one.
