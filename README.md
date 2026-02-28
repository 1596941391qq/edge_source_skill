# edge_source_skill

A practical skill for recommending high-value information sources from:
- Karpathy 92 long-form sources (`references/karpathy-92-hn-2025.tsv`)
- Local tactical source pool (`references/local-89-links.txt`)
- Six project tracks (`references/six-projects.md`)

The skill predicts `KnowledgeValue` per source and outputs a prioritized reading plan with risk notes for edge topics.

## Structure

- `SKILL.md`: trigger and workflow instructions
- `references/six-projects.md`: six-track classification
- `references/karpathy-92-hn-2025.tsv`: 92 curated long-form feeds
- `references/local-89-links.txt`: local tactical links
- `scripts/recommend_sources.py`: deterministic scoring/ranking engine

## What It Solves

- Recommend sources by user question, not fixed list
- Estimate likely knowledge value before reading
- Mix deep sources and tactical sources
- Flag risky domains/topics (blackhat/PBN/etc.) with explicit caution

## Quick Use

Run from repo root:

```bash
python scripts/recommend_sources.py "我在做AI SEO自动化，想找高质量来源帮助我设计合规SOP"
```

Example output includes:
- `问题归类`
- `问题标签`
- `推荐信源 Top 10`
- `风险提示` (when applicable)
- `优先阅读顺序`
- `实验建议`

## Edge Test Queries

- `我想研究PBN和寄生SEO路线，但要明确Google合规红线和风险边界`
- `我要做Instagram多账号矩阵，想找指纹浏览器和自动化风控相关信源`
- `我要做成人用品独立站品牌内容，想找选品和竞品叙事信源`
- `我在做Agent记忆层，想比较mem0/memobase和可解释检索评测方法`

## Notes

- `SKILL.md` can work alone as prompt instructions.
- Best results require keeping `scripts/` and `references/` together.
- High-risk sources are provided for boundary research, not direct copy/execution.
