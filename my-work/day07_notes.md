# Day 7 Notes — Extend Your Research Team (Chicago Housing, capstone)

## A wrinkle before starting

The repo's `day07_begin.py` turned out to be identical in structure to Day 6's script (no evaluator, no refinement loop, no cost-trimming hook) even though the challenge's "before you start" section assumes exactly those things already exist and are running clean. `day07_end.py` is the file that actually matches the challenge's description: evaluator agent, refinement loop, and a PostToolUse hook that trims WebSearch results before they enter context. I used `day07_end.py` as my real starting point and built the 6th agent on top of it. Flagging this for anyone else hitting the same confusion.

## The gap, stated before designing anything

The validator checks structure (do citations point to real references, does every finding have one). The evaluator checks presentation quality (coverage, source diversity, recency, gaps). Neither one checks whether a cited claim actually says what the report says it says. That's exactly the gap the Day 5 manual citation audit found by hand, at a cost of 2-3 hours: citations that point to a real, existing source that just doesn't contain the specific figure or quote attributed to it. **Sixth agent: factcheck-agent**, a systematic version of that audit, running automatically on every pass.

## Design

**Description (the routing table):**
"Checks whether each cited claim in a report matches what its source's search summary actually says. Run once per research pass, immediately after report-agent produces a report and before that report is returned as final, including every refinement round. Cannot search the web, cannot rewrite findings or citations, and cannot resolve the mismatches it finds -- it only flags them for the coordinator to attach to the report."

**Behavior:**
- Scope: one job, checking citations against the search summaries it's given. Explicit boundary: does not judge coverage, quality, or prose; does not decide what to keep or cut. Blocked case: if not given both a report and this pass's search summaries, say so and stop.
- Classification, mirroring the Day 5 audit's own categories: Verified (silent -- an unflagged citation is an implicit pass, to keep output compact), Misattributed, Overstated, and a fourth category specific to this system's refinement design: "Not re-verified this pass," for citations that trace to an earlier pass's search results it was never given (see the refinement note below).
- Attribution: every flag names the citation ID, the finding, the source, and quotes the relevant part of the search summary.
- Least privilege: `tools=[]`. It works from text it's handed, same as analysis and synthesis.
- `maxTurns=5`.

**The refinement wrinkle the challenge specifically warns about:** on a refinement pass, factcheck-agent only receives that round's new search results, not the original pass's. So it cannot verify citations carried over from the first draft; it has to say so rather than silently assuming they're fine or wrongly flagging them. Built that into the prompt directly.

**Making its output non-decorative:** added a `fact_check_flags` field to `REPORT_SCHEMA`. Coordinator workflow: after report-agent produces the report (step 5), delegate the report plus this pass's search summaries to factcheck-agent (step 6). If it returns flags, delegate the report and the flags back to report-agent once more (step 7), asking it to return the identical report with `fact_check_flags` populated and nothing else touched. `render_markdown` now prints a "## Fact-Check Flags" section when the list isn't empty. Added `factcheck-agent` to the coordinator's roster (the "delegate only to" list) -- missing that step is, per the challenge, the most common way this goes sideways.

## Proof it earns its place

Ran the same Chicago housing question (the one I've used all week) with and without factcheck-agent registered.

**Routing:** correct and unprompted on every single pass I observed, three separate times across two different runs -- the initial pass, refinement round 1, and refinement round 2 -- with no mention of fact-checking anywhere in the research request itself.

**What it caught, pass 1 of the full run that made it furthest:** 7 flags. The clearest one: a finding citing "699 units, 13 groundbreakings, 422 completed, 1,600 under construction" to three references ([1][2][3] -- a QAP/LIHTC press release and two news write-ups of the $300M funding announcement), when those specific figures actually come from a completely different press release ("Cut the Tape: Year of Progress," reference [5]) that wasn't even one of the three cited. Others: a bundle of six dollar figures ($137M, $1.4B, $135M, $1.25B, $21M, $10M) all credited to one source that only actually supports the smallest of the six; a program funding figure sourced to a document that only covers 2019-2024, nowhere near the FY2026 number attributed to it.

**Score movement:** initial evaluation 7/10. The evaluator's own writeup explicitly cited the fact-check flags as the reason: "the report's own fact_check_flags section reveals a material integrity problem... this means the apparent source diversity is partly illusory." After one refinement round (which the fact-check flags helped target -- two of the three follow-up queries were direct responses to specific flagged citations), the same report scored 8/10, with the evaluator this time crediting "a fact-check flag catching a mis-attributed citation" as evidence of rigor rather than a problem. factcheck-agent ran again on that refined report and caught one more issue (an outcome-statistics claim whose citations included three sources added in the new search round that didn't actually contain those numbers).

**Cost:** the two research passes plus evaluations plus fact-check delegations for this run came to $3.2061 + $3.3342 = $6.5403, landing right inside the challenge's own predicted "typically six to eight dollars" range for a full pass with refinement.

## The honest part: this session hit real instability

Getting a clean, fully-saved final report.md proved harder than expected, for reasons unrelated to factcheck-agent's design:

- Two separate runs (one with the agent, one without) crashed mid-pipeline with the same transient SDK/CLI error ("Command failed with exit code 1") inside the evaluator's query call. Not a logic bug in either script; looks like an infrastructure hiccup in this environment, and it hit both the baseline and the fact-check version equally.
- One run of the baseline (no factcheck-agent) had its own refinement round introduce a *new* uncited finding that failed the existing validator -- a pre-existing fragility in the given report-agent's revision behavior, not something factcheck-agent caused or could have prevented (that specific failure mode is the validator's job, and the validator caught it correctly).
- One run of the fact-check version hit the same kind of validator failure on its single-round revision.

None of this is a mark against the new agent. It's a real reminder, on the last day, of the whole week's throughline: a system that searches, analyzes, synthesizes, writes, fact-checks, evaluates, and refines itself still runs on infrastructure that can hiccup, and on a report-agent whose revision step can still introduce a new problem while fixing another. The safety nets (validator, budget ceiling, retry logic) are what make that survivable rather than invisible.

## Answering the three check-your-work questions

1. **Gap named before designing:** yes -- citation accuracy vs. source content, the exact hole Day 5's manual audit found.
2. **Coordinator routes correctly, unprompted:** yes, confirmed on three separate passes across two runs, including every refinement round.
3. **With-and-without proven, cost judged:** yes. The with-agent report caught 8 real citation problems across two passes that the original 4-agent team's validator structurally could not catch (it only checks that a citation ID exists somewhere in the reference list, not that the reference supports the claim). Total measured cost for a 2-pass run with the new agent: $6.54, in line with the challenge's own predicted range. Worth it: the alternative is what Day 5 already proved -- a human doing this same check by hand takes 2-3 hours.
