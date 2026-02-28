# edge_source_skill（中文）

[English README](./README.md)

这是一个用于“高深度信源推荐”的 skill，目标是帮助用户获得更广阔视野，包含 SEO/安全等边缘与对抗视角，并预测每个信源的知识价值。

## 数据来源

- `references/karpathy-92-hn-2025.tsv`（92 个长文深水信源）
- `references/deep-sources-github.tsv`（6 个高星深度入口型 GitHub 项目）

## 已内置的 6 个深水 GitHub 入口

1. https://github.com/sindresorhus/awesome
2. https://github.com/jivoi/awesome-osint
3. https://github.com/lockfale/OSINT-Framework
4. https://github.com/sbilly/awesome-security
5. https://github.com/meirwah/awesome-incident-response
6. https://github.com/papers-we-love/papers-we-love

## 使用方式

在仓库根目录执行：

```bash
python scripts/recommend_sources.py "我想研究更偏黑帽的SEO对抗思路，并评估可能后果"
```

输出包括：
- 问题标签
- Top 信源推荐与 `KnowledgeValue`
- 建议阅读顺序
- 可能后果（针对边缘/对抗方向）
- 24 小时可执行实验建议

## 说明

- 请保留 `SKILL.md + references + scripts` 一起使用。
- 本 skill 不做“固定答案”，而是基于问题动态匹配信源并给出价值预测。
