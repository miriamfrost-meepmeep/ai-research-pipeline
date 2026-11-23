# Day 6 Notes — Recover from a Failed Subagent (Chicago Housing question, for continuity with Days 1-5)

Question used (same as Day 5, for narrative continuity):
"Compare housing progress in Chicago across three fronts: new market-rate housing construction, city-funded affordable housing programs, and homelessness prevention initiatives -- which is showing the strongest measurable progress in 2026, and which is lagging?"

## Clean baseline

Run 1: subtype=success, is_error=False, 11 turns, cost $2.1900. Validation passed, report saved.
Run 2 (later, via the retry script with search restored): subtype=success, 10 turns, cost $1.9056. Attempt 1 succeeded, no retry needed.

Typical clean-run cost for this question: roughly **$2.05** (average of the two).

## Step 1-2: Sabotage and signal mapping

Changed SEARCH_AGENT's `tools=["WebSearch"]` to `tools=[]`. Single unmodified (no-retry) run.

Result: subtype=**success**, is_error=**False**, 5 turns, cost **$0.1084**. No rescue attempts this time, the coordinator delegated to search-agent exactly once per topic (3 total), got three honest "could not search" refusals, and let the pipeline continue straight through to a report with no findings. The ResultMessage gave no hint anything was wrong; the validator caught it immediately: "Report contains no findings."

Notably cleaner and cheaper than the earlier test on a different topic, where the coordinator burned 14 delegations trying to rephrase its way around the missing tool. Same sabotage, same coordinator prompt, different behavior. Worth being honest about: the "coordinator tries to rescue the run" behavior the challenge describes is real, but it isn't guaranteed to happen every time, on every topic.

## Step 3: Retry loop

Same retry loop as specified in the challenge (`run_with_retries`), plus the explicit `error_max_budget_usd` print.

## Step 4: Sabotaged retry runs

Ran the retry-enabled sabotaged script (`max_attempts=2`) with search still disabled:

- **Attempt 1**: subtype=success, 18 turns, cost $0.6045. This time the coordinator did probe a bit (12 search delegations plus one "diagnostic tool execution test" before giving up), but the resulting "findings" were all honest: "No verified data could be gathered on new market-rate housing...", "...on city-funded affordable housing...", "...on homelessness prevention...", plus one describing the diagnostic test itself. Failed validation because those are disclosures, not findings with citations, exactly as intended.
- **Attempt 2**: subtype=success, 16 turns, cost $0.3058. Same story, different specific phrasing: "Report contains no findings." Consistent failure.

Total cost across both failed attempts: **$0.91**. Both failures were honest. Nothing was fabricated in either attempt.

This matters as a direct comparison: in an earlier test of this same sabotage and this same retry loop, but on a different research question (AI coding assistant productivity), one retry attempt did not fail. It came back with a fully fabricated but structurally valid report, indistinguishable from a real one by any check the retry loop runs, at a cost close to a normal clean run. The search agent itself behaved honestly in isolation in both cases. The difference wasn't the search agent, it was what a downstream stage (analysis or synthesis) did when handed nothing but refusals, and that behavior wasn't consistent across topics or runs.

**The takeaway that survives both tests:** a validator built only on structure (are there findings, do citations resolve, are references used) cannot promise you honesty. It caught the honest failures here perfectly. It would not have caught the fabricated one if it had happened on this question instead. Retry logic like this is necessary. It is not sufficient.

## Step 4 (continued): Restored search tool

Restored `tools=["WebSearch"]`. Retry-enabled run, attempt 1: subtype=success, 10 turns, cost $1.9056. Clean recovery, no retries needed, consistent with the clean baseline.

Consistent with the challenge's framing: retries fix transient failures. They do nothing for a deterministic configuration problem, whichever way that problem happens to present that day.

## Step 5: Budget math

- `max_budget_usd` = $4.00 per attempt
- `max_attempts` = 2 (lowered from the script's default of 3, same reasoning as before: retries can't fix a configuration problem, so a 3rd attempt on a broken config rarely earns its keep)
- Worst case = 2 x $4.00 = **$8.00**
- Typical clean-run cost for this question: ~$2.05
- Worst case is roughly **3.9x** the typical cost

I'm comfortable with $8.00 as a worst case for a question that normally costs about $2. I would not have been comfortable with the original 3-attempt default, which put the worst case at $12, roughly 5.9x typical cost for this topic specifically.

One more honest number: total spend across every run in today's exercise (clean baseline x2, single sabotage, two-attempt sabotaged retry, restored retry) was **$2.19 + $0.1084 + $0.6045 + $0.3058 + $1.9056 = $5.11**, for the full sabotage-and-recovery exercise. Cheap, given what it demonstrated.
