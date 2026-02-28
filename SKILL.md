---
name: source-intel-recommender
description: Recommend high-depth sources for broad and edge-case learning (including adversarial SEO/security perspectives), using Karpathy's 92 feeds and curated deep GitHub source maps. Use when user asks for 信源推荐, 边缘玩法研究入口, 深水论坛/论文/情报入口, or wants predicted knowledge value.
---

# Source Intel Recommender

## When To Use
Use this skill when the user asks:
- 针对某个问题推荐高价值信源
- 想要更广视野，尤其是边缘/对抗思路
- 先看什么、后看什么最有效
- 这些来源可能带来什么知识价值

## Inputs
- User question and constraints (time, language, risk appetite, build stage)
- `references/karpathy-92-hn-2025.tsv`
- `references/deep-sources-github.tsv`

## Workflow
1. Detect query focus tags (SEO/PSEO/GEO, adversarial, OSINT, security, research, automation, commerce).
2. Build candidate pool:
- Karpathy 92 long-form feed list (depth baseline)
- Deep GitHub source maps (entry points for high-signal communities and docs)
3. Score each source on 1-5:
- `Relevance`: fit to query intent
- `Depth`: insight density / first-principles value
- `Actionability`: can turn into testable workflow quickly
- `Freshness`: likely still useful now
- `Consequence`: potential downside if copied blindly (higher score = better controllability)
4. Compute `KnowledgeValue`:
- `KnowledgeValue = 0.30*Relevance + 0.25*Depth + 0.25*Actionability + 0.10*Freshness + 0.10*Consequence`
5. Output top recommendations:
- Why source fits
- What likely value it unlocks
- Reading order (fast execution -> deep method -> adversarial counterexample)
- Potential consequences (account risk, ranking volatility, reputation, legal exposure) when relevant

## Output Format
1. `问题标签`: <comma-separated tags>
2. `推荐信源 Top N`:
- `<source>` | `KnowledgeValue: x.x/5` | `预计知识价值`: <one sentence>
- ...
3. `优先阅读顺序`: <3-5 items>
4. `可能后果`: <only when query has edge/adversarial intent>
5. `实验建议`: <1 action in 24h>

## Heuristics
- Prefer high-signal entry maps over random tactic posts.
- For adversarial topics, explain likely consequences instead of only binary prohibition wording.
- Mix at least one deep methodology source and one executable source map.
