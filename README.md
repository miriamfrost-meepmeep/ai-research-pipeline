# AI Research Pipeline: what citations hide

A team of Claude agents researches Chicago housing and writes a cited report. I checked every citation by hand, broke the system on purpose and designed a sixth agent to catch what the checks were missing.

**Built by:** Miriam Frost, product manager · [Portfolio](https://miriamfrost-meepmeep.github.io) · [LinkedIn](https://www.linkedin.com/in/miriam-frost-productmanager/)
**Course:** Kesha Williams, [*Claude Agents: Build a Multi-Agent Research System in 7 Days*](https://www.linkedin.com/learning/claude-agents-build-a-multi-agent-research-system-in-7-days) (LinkedIn Learning)
**Status:** Learning project. Not a production system.

**Read the case study first:** [CASE_STUDY.md](CASE_STUDY.md)

## What's the course's and what's mine

This repo is a fork of the course's exercise files. The `DAY01` to `DAY07` folders are the course's code, unchanged. My work is in `my-work/`.

| | Course | Mine |
| --- | --- | --- |
| Five-agent system (search, analysis, synthesis, report, coordinator) | ✓ | |
| Validator, evaluator, retry loop, budget caps | ✓ | |
| Daily challenges, including the Day 6 sabotage step | ✓ | |
| Research question: Chicago housing progress in 2026 | | ✓ |
| Day 4: synthesis rule so minority findings aren't dropped | | ✓ |
| Day 5: hand audit of all 45 citations | | ✓ |
| Day 6: retries lowered from 3 to 2, budget-trip warning | | ✓ |
| Day 7: sixth agent design (fact-checker), its prompt and categories | | ✓ |
| Every number in the case study | | ✓ |

## Results

- **Day 5:** 21 of 45 citations (47%) checked out. 12 misattributed, 6 overstated, 4 fabricated or dead, 2 couldn't be checked.
- **Day 6:** On an earlier test question, a retry produced a fully fabricated report with 25 references. It passed every check. Lowering retries from 3 to 2 cut the worst case from $12 to $8.
- **Day 7:** My fact-check agent flagged 7 citations on the first pass and 1 more on the second. 8 across two passes of one run. Score went from 7 to 8 out of 10. The run cost $6.54.

## What's in `my-work/`

| File | What it is |
| --- | --- |
| `day04_synthesis_rule.py` | Day 4 with my rule: a minority or opposing finding counts as a conflict and gets its own confidence level. Also prints each agent's result so I could see what it returned. |
| `day05_report.md` | The Day 5 report I audited. |
| `day05_citation_audit.md` | My audit of all 45 citations, claim by claim. |
| `day05_citation_list.md` | All 45 sources with links. |
| `day06_retry_housing.py` | Day 6 retry loop on my question. Retries set to 2, plus a warning when the budget cap trips. |
| `day06_retry_first_topic.py` | Same script on the earlier test question, where the fabricated report came from. |
| `day06_notes.md`, `day06_notes_first_topic.md` | Run-by-run notes from the sabotage tests. |
| `day07_with_factcheck.py` | The full system plus my sixth agent, built on the course's `day07_end.py`. |
| `day07_notes.md` | How I designed it, what it caught, what it cost. |

## Run it

You need Python 3.10 or later and an Anthropic API key.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here   # Windows: set ANTHROPIC_API_KEY=your-key-here
python my-work/day07_with_factcheck.py
```

Every run makes real API calls. A full Day 7 run with refinement cost me about $6.50.

## Limits

- One research question, one topic.
- 8 flags across two passes of one run. A small sample.
- I haven't measured what the fact-check agent missed.
- Two runs crashed with the same SDK error inside the evaluator, so my with-and-without comparison is incomplete.
- Costs come from the SDK's estimates, not billing data.

## License

The course files are LinkedIn Learning exercise files. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
