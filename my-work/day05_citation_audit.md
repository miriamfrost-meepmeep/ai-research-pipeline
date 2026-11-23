# Day 5 Citation Audit — Chicago Housing Progress Report (2026)

Question run through the full search → analysis → synthesis → report pipeline:
"Compare housing progress in Chicago across three fronts: new market-rate housing construction, city-funded affordable housing programs, and homelessness prevention initiatives -- which is showing the strongest measurable progress in 2026, and which is lagging?"

Pipeline cost: $2.5492 | 9 turns | Report: 45 citations across 3 fronts

## Pre-audit finding: coordinator rule violation

Before auditing a single citation, the coordinator's own output (`message.result`, what the script saves to `report.md`) turned out to be a paraphrased, shortened rewrite of the report-agent's actual output — missing the entire References section and the "Unresolved Conflicts and Data Caveats" section. This directly violates the coordinator's own rule 6: "Output the report exactly as report-agent returned it. Do not edit, summarize, or reformat it." The report-agent's true output (captured via the Task tool result, not the top-level result) was restored and used for this audit. Any Day 5 script that trusts `message.result` for the final report will silently ship a report with no citations.

## Structural checks

- All 45 reference numbers are used at least once in the body. No unused references.
- No citation number appears in the body that isn't defined in the References list.
- All 45 URLs trace back to something a search agent actually returned — no citation was invented by the report agent from nothing.
- One factual claim in Findings carries no citation at all: "Rapid Rehousing has cumulatively housed more than 3,350 people and was permanently funded at $5.1 million in the 2026 budget" (Front C). It sits next to a [39]-cited sentence but isn't itself tagged.

## Classification of all 45 citations

| # | Source | Classification | Note |
|---|---|---|---|
| 1 | MMG Q3 2025 Pipeline Report | Misattributed | Live page shows placeholder "0" aggregate stats; none of the cited figures (11,000 units, 1.9%, 40% YoY, 70% luxury) appear |
| 2 | Matthews Q1 2026 Report | Misattributed (partial) | 9,800-units figure confirmed; 56.6%/31,054-unit downtown breakdown not on page |
| 3 | MMG Q4 2025 Pipeline Report | Overstated | Raw data table with no trend narrative; cited as "confirming continued moderation" |
| 4 | MMG Q2 2026 Pipeline Report | Overstated | Same issue; page explicitly neither confirms nor contradicts a moderation trend |
| 5 | Essex Capital Markets | Verified | "Smallest pipeline in more than a decade" confirmed near-verbatim |
| 6 | The Real Deal, Sept 1 2026 | Inconclusive | 403 on fetch; headline confirmed to exist elsewhere — likely bot-blocked, not fabricated |
| 7 | The Real Deal, Sept 15 2025 | Verified | Framing matches |
| 8 | Cushman & Wakefield Marketbeat | Verified | 3.2% YoY rent growth confirmed exactly |
| 9 | Yardi Matrix 2026 | Misattributed | 3.3% figure absent; source's actual completions-decline figure is ~31%, not 60% |
| 10 | Crain's "Downtown rents jump..." | Fabricated | URL resolves to an unrelated article |
| 11 | Crain's "Trends to Watch 2026" | Fabricated | Same unrelated redirect as #10 |
| 12 | The Real Deal, "Units Up 12%" | Verified | All sub-figures confirmed |
| 13 | Chicago.gov QAP/LIHTC release | Verified (core) / Misattributed (sub-claim) | $300M/1,223 units confirmed; the "3,400+ units since Johnson" figure is not in this release |
| 14 | Chicago YIMBY | Verified | |
| 15 | Block Club Chicago | Verified | |
| 16 | CHA FY2026 budget | Verified | |
| 17 | Chicago Defender | Verified | |
| 18 | CHA Development Update | Misattributed | $4M Lathrop loan confirmed; "44 Restore Home properties" not on this page |
| 19 | CHA "Year of Renewal" | Misattributed | Neither Grace Manor nor Westhaven Park Station appears on this page |
| 20 | 2025 CAPER (Draft) | Inconclusive | Network-blocked (chicago.gov); plausibly real |
| 21 | The Real Deal, TIF funding | Misattributed | TIF/downtown-skew finding confirmed; the "12% of bond committed" figure is not in this article |
| 22 | Block Club Chicago, TIF | Misattributed | Same gap; also word-for-word identical to #21 and #23 |
| 23 | Chicago Sun-Times, TIF | Fabricated (as cited) | Cited URL uses a typo'd slug that doesn't resolve; correct URL exists but still lacks the 12% figure |
| 24 | Block Club, voucher waitlist | Verified | |
| 25 | Illinois Policy Institute, $700K/unit | Verified | Exact match ($695,682 rounds to ~$700K) |
| 26 | Block Club, cost escalation | Verified | |
| 27 | Cut the Tape tracker | Misattributed | Live tracker doesn't show a 90% figure; that stat actually belongs to #30 |
| 28 | The Real Deal, "inept" | Overstated | No developer is quoted using the word "inept" — not in the source |
| 29 | Illinois Policy Institute, red tape | Overstated | Dated April 2025, presented as bearing on 2026 |
| 30 | Metropolitan Planning Council | Misattributed | Dated April 2025, not 2026 as labeled; is the true source of the 90%/107 figure wrongly attributed to #27 |
| 31 | Crain's, CHA ouster | Misattributed | Target was CHA Board Chairman Matthew Brewer, not the CEO |
| 32 | FHLBank Chicago | Verified | |
| 33 | Block Club, database ordinance | Overstated | Real legislation name is "Accountable Housing and Anti-Discrimination Waitlist Ordinance," not "...Act" |
| 34 | WTTW, Sept 2026 PIT count | Verified | All three sub-claims (6,527, unsheltered +25%, 66% Black) confirmed |
| 35 | Chicago.gov PIT press release | Fabricated | Search agent's own summary shows this announces the count's *launch* in January, not its September results — logically can't be the source of the 6,527 figure |
| 36 | DFSS 2025 Annual Report | Verified (indirect) | Corroborated by #37; math checks out |
| 37 | WTTW, July 2025 | Verified | |
| 38 | Reason Magazine | Overstated | National piece; Chicago mentioned once in passing, not a Chicago-specific causal claim |
| 39 | 2025 CAPER (Final) | Inconclusive | Network-blocked; adjacent $5.1M/3,350-person claim is uncited regardless |
| 40 | Chicago Coalition to End Homelessness | Misattributed | Page doesn't mention CBRAP or an Eviction Counsel Program at all |
| 41 | WBEZ | Verified | |
| 42 | CBS News Chicago | Verified | |
| 43 | CCEH statement | Verified | Fair paraphrase, not a literal quote |
| 44 | City Bureau | Verified | Minor date discrepancy ("until 2025" vs. "by end of 2026") |
| 45 | Chicago Sun-Times, Bring Chicago Home | Verified | |

**Totals: 21 Verified, 12 Misattributed, 6 Overstated, 4 Fabricated/dead-link, 2 Inconclusive (network-blocked) = 45**

Verified rate: 21/45 = **47%**

## Stage tracing

The dominant failure category is Misattributed (12 of 45), and tracing it back through the raw search-agent output shows the root cause is almost never downstream re-tagging by analysis or synthesis. It's the search agent itself:

- The search agent's own two-sentence summaries already contain the fabricated statistics (MMG Q3 pipeline stats, Yardi's 3.3%/60% figures), the invented quote ("inept"), the wrong legislation name, and the mislabeled role ("CHA CEO" when the source's own headline is about the Board Chairman). Every one of these was carried forward unchanged and faithfully by analysis, synthesis, and report — those stages did their job correctly on bad input.
- One clear exception: the [21]/[22]/[23] "corroborated by three independent outlets" framing was written by the synthesis agent itself. All three are republications of one syndicated NYT investigation (same byline, same quotes), not independent reporting. This is the same corroboration-honesty failure from Day 4, showing up again because this is an unmodified Day 5 script without that fix.
- One clear analysis/synthesis-stage tagging error: reference [35] (a press release announcing the count's launch) got credited with reporting the count's results, which weren't published until 8 months later by a different source.

## How the fabrication actually happens

The stage tracing above points at the search agent as the source of most Misattributed and Fabricated citations. To find out why, rather than just where, I ran the exact query behind one of the clearest cases directly: the MMG Q3 2025 Pipeline Report citation ([1]), which claimed 11,000 units under construction, 1.9% of inventory, a 40% year-over-year decline, and a 70% luxury share — none of which are on the live page.

Query tested: "Chicago Q3 2025 Pipeline Report MMG multifamily units under construction"

Result: 9 sources returned, every one a bare title and URL. No snippet, no description, no preview text of any kind — nothing for the model to read a number out of, correctly or incorrectly.

That rules out the more forgivable explanation (misreading a thin-but-present snippet, mixing up two nearby figures) and points at the harsher one: the search agent had zero retrieved numeric content for that source and generated four specific, internally consistent statistics anyway, driven by what a page titled "Q3 2025 Pipeline Report" would plausibly say rather than by anything it actually saw.

One caveat on this test: I ran it with the WebSearch tool available to me in this environment, not the exact internal call the Day 5 search-agent's Claude Agent SDK session made. I can't prove the two returned byte-for-byte identical results. But the pattern — search results with no snippet content — lines up exactly with what would produce this failure, so I'm treating it as strong inference rather than confirmed fact.

The takeaway this adds to the audit: the failure mode isn't "the AI got a number slightly wrong." It's "the AI had nothing and produced a number anyway, formatted exactly like every other verified citation in the report." Nothing about how a fabricated citation looks on the page distinguishes it from a real one — same format, same confidence, same specificity. That's what makes citation count a bad proxy for report quality, and it's the business case for Day 6: this kind of check has to run automatically, because it isn't visually detectable.

## Fix applied and verified

Added accuracy rules to the search-agent prompt: only report a figure if it's actually visible in retrieved content, flag when it isn't rather than filling the gap, never present a paraphrase as a direct quote, and copy exact names/titles rather than inferred roles.

Reran just the search-agent stage (not the full pipeline) on the worst-performing topic. Result: genuine but partial improvement. The agent now explicitly hedges when it can't confirm a figure ("Specific figures from the report body were not visible in the retrieved search content") — behavior that didn't exist at all in the original run. But a spot-check on one new claim (MMG's Q2 2026 report, again a JS-rendered dashboard page showing placeholder zeros) showed it still fabricated a full set of aggregate statistics despite the new rule. The instruction reduced the failure rate; it didn't eliminate it, especially against a page whose visible content is just placeholder zeros in a data table.

## Cost and time (Step 6)

- Citations checked: 45
- Pipeline cost: $2.5492 (full run) + $0.1987 (isolated fix verification) = $2.75 total
- Wall-clock time for AI-assisted verification: approximately 10 minutes, using 4 parallel verification passes plus targeted follow-ups
- Actual time spent manually checking these same citations by hand (opening each link, comparing it against the claim): well over 2 hours, close to 3
- That's roughly 15-18x longer than the AI-assisted pass, for a $2.75 pipeline cost — the real business case for Day 6's automation isn't hypothetical, it's the gap between "10 minutes and $2.75" and "a full afternoon"
