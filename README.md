# edge_source_skill

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Sources](https://img.shields.io/badge/Sources-150%2B-orange.svg)](#data-sources)
[![Part of Pipeline](https://img.shields.io/badge/Pipeline-1%20of%203-6e40c9.svg)](#pipeline)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**AI-powered source intelligence recommender** — find high-depth information sources for edge knowledge, adversarial SEO, and OSINT research.

> [中文说明](./README.zh-CN.md)

## What It Does

Give it a research question, get back a scored, ranked list of information sources with reading order and predicted knowledge value.

```bash
python scripts/recommend_sources.py "I want adversarial SEO sources to understand edge mechanics"
```

Output:
- **Query tags** — auto-detected topic clusters
- **Top sources** — scored on Relevance × Depth × Actionability × Freshness × Consequence
- **Reading order** — fast execution → deep method → adversarial counterexample
- **Knowledge gaps** — missing source types to expand coverage
- **24h experiment** — one actionable test you can run today

## Pipeline

This is **Stage 1** of a 3-stage content intelligence pipeline:

```
edge_source_skill ──→ EdgeKnowledge_Skill ──→ anything-to-md
   (find sources)       (crawl & analyze)        (convert to MD)
```

| Stage | Repo | What it does |
|---|---|---|
| 1 — Find | **edge_source_skill** | Recommend high-value sources for a topic |
| 2 — Crawl | [EdgeKnowledge_Skill](https://github.com/1596941391qq/EdgeKnowledge_Skill) | Deep-crawl forums, Reddit, communities |
| 3 — Convert | [anything-to-md](https://github.com/1596941391qq/anything-to-md) | Convert any content to LLM-ready Markdown |

## Data Sources

| File | Contents |
|---|---|
| `references/karpathy-92-hn-2025.tsv` | 92 long-form high-signal feeds curated by Karpathy |
| `references/deep-sources-github.tsv` | Expanded deep-source GitHub projects (awesome lists, OSINT frameworks, security tools) |
| `references/deep-sources-telegram.tsv` | Telegram channel pool (continuously importable) |

### Included Deep GitHub Sources

awesome · awesome-osint · OSINT-Framework · awesome-security · awesome-incident-response · papers-we-love · awesome-selfhosted · awesome-sysadmin · awesome-privacy · awesome-threat-detection · awesome-browser-security · awesome-malware-analysis · awesome-devsecops

## Scoring Formula

```
KnowledgeValue = 0.30×Relevance + 0.25×Depth + 0.25×Actionability + 0.10×Freshness + 0.10×Consequence
```

Each dimension scored 1–5. Sources ranked by weighted KnowledgeValue.

## Telegram Integration (Optional)

```bash
pip install telethon
```

```bash
export TG_API_ID=your_id
export TG_API_HASH=your_hash

python scripts/import_telegram_sources.py --query "seo blackhat osint" --limit 30 --tags "telegram,seo,adversarial"
```

Imported channels auto-merge into the recommendation pool.

## Quick Start

```bash
git clone https://github.com/1596941391qq/edge_source_skill.git
cd edge_source_skill
pip install -r requirements.txt  # or just run — minimal deps
python scripts/recommend_sources.py "your research question here"
```

## Related Projects

- [EdgeKnowledge_Skill](https://github.com/1596941391qq/EdgeKnowledge_Skill) — Stage 2: deep-crawl the sources this tool recommends
- [anything-to-md](https://github.com/1596941391qq/anything-to-md) — Stage 3: convert crawled content to clean Markdown
- [bypass-anything](https://github.com/1596941391qq/bypass-anything) — Anti-detection layer for browser automation
- [nichedigger](https://github.com/1596941391qq/nichedigger) — Reddit-powered keyword mining for PSEO
