import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AgentDefinition,
    AssistantMessage,
    UserMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
    ResultMessage,
)

SEARCH_AGENT = AgentDefinition(
    description=(
        "Searches the web for credible sources on one specific topic. "
        "Use whenever a task requires finding new information."
    ),
    prompt="""You are a research search agent.
            Search the web for the topic you are given.
            Find at least five distinct, credible sources.
            For each source report the title, URL, publication date if available,
            and a two-sentence summary.
            Do not analyze or draw conclusions. Just search and report.""",
    tools=["WebSearch"],
)

ANALYSIS_AGENT = AgentDefinition(
    description=(
        "Analyzes ONE set of sources on ONE topic and extracts key "
        "findings. Use once per search result set. Cannot search the web."
    ),
    prompt="""You are a research analysis agent.
              You receive sources found by a search agent on a single topic.
              Extract the key findings:
              - The main claims, each tagged with which sources support it
              - Points where sources disagree, quoted or closely paraphrased
              - Gaps the sources do not cover
              Preserve source attribution on every claim. Do not resolve
              disagreements. Report them faithfully for the synthesis agent.
              Do not search the web.""",
    tools=[],
)

SYNTHESIS_AGENT = AgentDefinition(
    description=(
        "Combines multiple analyses into one unified picture and "
        "resolves conflicts between them. Use exactly once, after all "
        "analyses are complete. Cannot search the web."
    ),
    prompt="""You are a research synthesis agent.
            You receive analyses of several topics, each containing claims,
            disagreements, and gaps. Produce one unified synthesis:

            1. State the overall picture that emerges across all analyses.
            2. For every conflict between sources, resolve it explicitly:
              - Prefer claims corroborated by multiple independent sources.
              - Prefer more recent sources when facts change over time.
              - Prefer primary sources over secondary reporting.
              - If the conflict cannot be resolved, say so and present
                both positions with their support. Never split the
                difference or average competing numbers.
            3. Do not dismiss a counterbalancing, minority, or affirmative
              finding as "not a real conflict" just because it fails to
              contradict every other source. If any source reports a real
              benefit, a reversed effect, or a subgroup for whom the
              dominant conclusion does not hold, treat it as a conflict:
              apply one of the four resolution rules above to it explicitly
              and give it its own confidence level, rather than folding it
              silently into the majority conclusion as a mere difference
              of "emphasis."
            4. Attach a confidence level (high, medium, low) to each major
              conclusion, with one line explaining why.
            5. Carry forward every unresolved gap. Do not let gaps disappear.

            Work only from the analyses you are given.""",
    tools=[],
)

COORDINATOR_PROMPT = """You are a research coordinator managing a team
of specialist agents.

When you receive a research request:
1. Break it into focused subtasks.
2. Delegate each search subtask to search-agent, one topic per delegation.
3. Delegate each result set to analysis-agent, one analysis per topic.
4. Delegate ALL completed analyses to synthesis-agent in a single
   delegation. Include every analysis in full.
5. Present the synthesis as the final answer, and report which
   agent handled each part.

Never search, analyze, or synthesize yourself. Your job is
delegation and assembly."""


def _extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)
    return ""


async def run_research(request: str) -> None:
    options = ClaudeAgentOptions(
        system_prompt=COORDINATOR_PROMPT,
        agents={
            "search-agent": SEARCH_AGENT,
            "analysis-agent": ANALYSIS_AGENT,
            "synthesis-agent": SYNTHESIS_AGENT,
        },
        allowed_tools=["Agent", "WebSearch"],
        setting_sources=[],
        max_budget_usd=4.00,
        model="claude-sonnet-5",
        fallback_model="claude-haiku-4-5-20251001",
        max_turns=40,
    )

    pending_labels = {}

    async for message in query(prompt=request, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock) and block.name in ("Agent", "Task"):
                    agent = block.input.get("subagent_type", "unknown")
                    task = block.input.get("description", "")
                    pending_labels[block.id] = (agent, task)
                    print(f"\n--> Delegating to {agent}: {task}")
                    print("=" * 70)
                elif isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, UserMessage):
            content = message.content
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, ToolResultBlock):
                        label = pending_labels.get(block.tool_use_id)
                        text = _extract_text(block.content)
                        if label and text:
                            agent, task = label
                            print(f"\n<== Result from {agent} ({task}):")
                            print("-" * 70)
                            print(text)
                            print("-" * 70)
        elif isinstance(message, ResultMessage):
            print(f"\nDone in {message.num_turns} turns.")
            print(f"Estimated cost: ${message.total_cost_usd:.4f}")


if __name__ == "__main__":
    asyncio.run(
        run_research(
            "Do open-plan offices help or hurt collaboration? Look at "
            "the evidence on face-to-face interaction, employee "
            "productivity, and employee wellbeing/satisfaction."
        )
    )
