# edge_source_skill

[中文说明 (README.zh-CN.md)](./README.zh-CN.md)

A skill for recommending high-depth information sources to broaden perspective, including adversarial SEO/security viewpoints.

## Data Sources

- `references/karpathy-92-hn-2025.tsv` (92 long-form feeds)
- `references/deep-sources-github.tsv` (expanded deep-source GitHub entry projects)
- `references/deep-sources-telegram.tsv` (Telegram deep-source pool, continuously importable)

## Included Deep GitHub Sources

- https://github.com/sindresorhus/awesome
- https://github.com/jivoi/awesome-osint
- https://github.com/lockfale/OSINT-Framework
- https://github.com/sbilly/awesome-security
- https://github.com/meirwah/awesome-incident-response
- https://github.com/papers-we-love/papers-we-love
- https://github.com/awesome-selfhosted/awesome-selfhosted
- https://github.com/awesome-foss/awesome-sysadmin
- https://github.com/sindresorhus/awesome-privacy
- https://github.com/0x4D31/awesome-threat-detection
- https://github.com/vFense/awesome-browser-security
- https://github.com/rshipp/awesome-malware-analysis
- https://github.com/gmelodie/awesome-devsecops

## Usage

```bash
python scripts/recommend_sources.py "I want adversarial SEO sources to understand edge mechanics and likely consequences"
```

Output includes:
- query tags
- Top source recommendations with `KnowledgeValue`
- reading order
- likely consequences for edge/adversarial directions
- missing source-list types to further expand deep-zone coverage
- 24h experiment suggestion

## Optional Telegram Integration

1. Install dependency:
```bash
pip install telethon
```
2. Set env vars: `TG_API_ID`, `TG_API_HASH` (optional `TG_SESSION`)
3. Import channels:
```bash
python scripts/import_telegram_sources.py --query "seo blackhat osint" --limit 30 --tags "telegram,seo,adversarial"
```
4. Re-run recommender; Telegram sources are included automatically.

## Notes

- Keep `SKILL.md`, `references/`, and `scripts/` together.
- The skill explains likely consequences for edge tactics to support better decisions.
