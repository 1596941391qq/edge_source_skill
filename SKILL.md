---
name: source-intel-recommender
description: Recommend high-value information sources based on user questions, using six project tracks plus Karpathy's 92 HN-curated feeds and local source links. Use when user asks for 信源推荐, 信息源优先级, 资料怎么找, or wants predicted knowledge value before reading.
---

# Source Intel Recommender

## When To Use
Use this skill when the user asks:
- 哪些信源值得看
- 针对某个问题推荐信息源
- 先看什么、后看什么
- 这些来源能带来什么知识价值

## Inputs
- User question and constraints (time, language, risk tolerance, budget)
- `references/six-projects.md`
- `references/karpathy-92-hn-2025.tsv`
- `references/local-89-links.txt`

## Workflow
1. Classify the question into one or two project tracks from `six-projects.md`.
2. Build candidate sources:
- Start from Karpathy-92 list (long-form depth baseline).
- Add local links as tactical/market context.
3. Score each candidate (1-5):
- `Relevance`: task fit
- `Depth`: original insight density
- `Actionability`: can become SOP/experiment quickly
- `Freshness`: likely still valid now
- `Risk`: compliance/quality risk (reverse score; high risk -> low)
4. Compute `KnowledgeValue`:
- `KnowledgeValue = 0.30*Relevance + 0.25*Depth + 0.25*Actionability + 0.10*Freshness + 0.10*Risk`
5. Return top recommendations with predicted value:
- Why this source fits the exact question
- What specific knowledge likely extractable
- Suggested reading order (quick win -> deep dive -> validation)
- One warning if source quality/compliance is uncertain

## Output Format
Use this exact structure:

1. `问题归类`: <project-track>
2. `推荐信源 Top N`:
- `<source>` | `KnowledgeValue: x.x/5` | `预计知识价值`: <one sentence>
- ...
3. `优先阅读顺序`: <3-5 items>
4. `实验建议`: <1 next action within 24h>

## Heuristics
- Prefer primary sources (official docs, original blogs, repos) over reposts.
- For SEO/PSEO/GEO, add explicit compliance note.
- For AI tooling/workflow, include one architecture source + one execution source + one case source.
- If user gives a niche geo/industry, prioritize sources with domain evidence and recent updates.

## Assumptions For This Workspace
The six project tracks are mapped from local recap topics A-F. If user provides a different "six projects" list, replace mapping immediately and keep the same scoring workflow.
