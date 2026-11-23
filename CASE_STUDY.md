# AI Research Pipeline: what citations hide

Miriam Frost, September 2026. Built through Kesha Williams' LinkedIn Learning course, *Claude Agents: Build a Multi-Agent Research System in 7 Days*. The five-agent system and the daily challenges are the course's. The research question, the audits, the sixth agent's design and every number below are mine.

## What I built

A research team of Claude agents, built with the Claude Agent SDK. A coordinator delegates to a search agent, an analysis agent, a synthesis agent and a report agent. A validator checks the report's structure. An evaluator scores it out of 10 and sends weak reports back for another round. Budget caps and a retry loop keep a bad run from running up a bill.

I ran the same question all week: *Compare housing progress in Chicago across new market-rate construction, city-funded affordable housing, and homelessness prevention. Which is showing the strongest measurable progress in 2026, and which is lagging?*

## Day 5: I checked every citation by hand

The report looked authoritative. It had 45 citations across three topics. I opened every link and compared it to the claim.

| Result | Citations |
| --- | --- |
| Verified | 21 |
| Misattributed: real source, but it doesn't say that | 12 |
| Overstated | 6 |
| Fabricated or dead link | 4 |
| Couldn't check (blocked site) | 2 |

**Only 21 of 45 (47%) checked out.** Every citation pointed to a real reference. The structure was perfect. The content often wasn't.

Two more things I found:
- The coordinator was supposed to return the report exactly as written. It shortened it instead and dropped the whole References section. Any script that trusted that output would have shipped a report with no citations.
- I added accuracy rules to the search agent's prompt. It started hedging when it couldn't confirm a figure. It still made up statistics from one page that showed only placeholder zeros. The rule reduced the problem. It didn't fix it.

**Cost of checking by hand:** 2 to 3 hours for 45 citations.

## Day 6: I broke it on purpose

The course had me remove the search agent's only tool and watch what happened.

On my housing question, the failures were honest. The search agent said it couldn't search. The report came back empty. The validator caught it every time.

On an earlier test with a different question, one retry came back with a **fully fabricated report**: 16 findings, 25 references to real, well-known studies, and a cost close to a normal run. The search agent had no tools the whole time, so every source was invented. It **passed every check**.

That's the finding of the week: **a validator that checks structure cannot tell a fabricated report from a real one.** Retries help with flaky failures. They can't fix a broken setup, and they can't catch a convincing lie.

I also lowered the retry attempts from 3 to 2. That cut the worst-case cost from $12 to $8, about 4 times a normal $2 run instead of 6.

## Day 7: I designed a sixth agent

The capstone asked for a sixth specialist, designed from scratch. The course offered five options. I chose a **fact-check agent**, because Day 5 had shown me exactly what it needed to catch.

**My design:**
- **One job:** check each cited claim against what its source actually says. It doesn't judge quality or rewrite anything. It only flags.
- **No tools.** It works from the search results it's handed.
- **Four categories,** matching my Day 5 audit, plus one I added: *"Not re-verified this pass."* On a refinement round it only sees that round's new search results, so it has to say when it can't check an older citation instead of quietly passing it.
- **Its flags go into the report.** A specialist whose findings go nowhere is decoration.

**What it caught on the first pass: 7 flags.** For example:
- A finding cited three sources for "699 units, 13 groundbreakings, 422 completed, 1,600 under construction." Those figures came from a different press release that wasn't cited at all.
- Six dollar figures, from $10M to $1.4B, credited to one source that supports only the smallest.

It caught **1 more on the second pass**: 8 across two passes of one run.

**Did it earn its place?**

| | Result |
| --- | --- |
| Routing | The coordinator called it correctly, unprompted, on all 3 passes I watched |
| Evaluator score | 7 out of 10 on the first pass. The evaluator named the fact-check flags as the reason. 8 out of 10 after one refinement round |
| Refinement | 2 of the 3 follow-up searches went after citations it had flagged |
| Cost | $6.54 for the two-pass run, inside the course's predicted $6 to $8 |
| Versus doing it by hand | Every pass, automatically, instead of 2 to 3 hours |

## What didn't work

- **Two runs crashed** with the same SDK error inside the evaluator, one with the fact-check agent and one without. That's an infrastructure problem, not a design one, but it means my clean with-and-without comparison is incomplete.
- **Refinement can break things.** Twice, a refinement round added a new uncited finding. The validator caught both. The fact-check agent can't prevent that kind of error.
- **The fact-check agent only knows what it's given.** It checks claims against search summaries, not the full source pages. A summary that's wrong will pass.

## What I learned as a product manager

- **Citation count is a bad stand-in for quality.** A fabricated citation looks exactly like a real one: same format, same confidence.
- **Measure by hand first.** The 2 to 3 hour audit told me exactly what to automate and how to judge whether the automation was working.
- **Every check catches only what it was built to catch.** Structure, quality and truth are three different checks.

## Limits

- One research question, one topic.
- 8 flags across two passes of one run. That's a small sample.
- I haven't measured what the fact-check agent missed.
- Costs are estimates from the SDK, not billing data.
