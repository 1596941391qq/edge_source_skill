# edge_source_skill

[中文说明 (README.zh-CN.md)](./README.zh-CN.md)

A skill for recommending high-depth information sources to broaden perspective, including adversarial SEO/security viewpoints.

## Data Sources

- `references/karpathy-92-hn-2025.tsv` (92 long-form feeds)
- `references/deep-sources-github.tsv` (6 high-star deep-source GitHub entry projects)

## Included Deep GitHub Sources

- https://github.com/sindresorhus/awesome
- https://github.com/jivoi/awesome-osint
- https://github.com/lockfale/OSINT-Framework
- https://github.com/sbilly/awesome-security
- https://github.com/meirwah/awesome-incident-response
- https://github.com/papers-we-love/papers-we-love

## Usage

```bash
python scripts/recommend_sources.py "I want adversarial SEO sources to understand edge mechanics and likely consequences"
```

Output includes:
- query tags
- Top source recommendations with `KnowledgeValue`
- reading order
- likely consequences for edge/adversarial directions
- 24h experiment suggestion

## Notes

- Keep `SKILL.md`, `references/`, and `scripts/` together.
- The skill explains likely consequences for edge tactics to support better decisions.
