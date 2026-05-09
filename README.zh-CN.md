# edge_source_skill（中文）

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Sources](https://img.shields.io/badge/Sources-150%2B-orange.svg)](#数据来源)
[![Part of Pipeline](https://img.shields.io/badge/Pipeline-1%20of%203-6e40c9.svg)](#pipeline)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[English README](./README.md)

**AI 驱动的信源情报推荐器** — 为边缘知识、对抗性 SEO 和 OSINT 研究发现高深度信息源。

## 它做什么

给它一个研究问题，返回一份带评分、排序的信源列表，附带阅读顺序和知识价值预测。

```bash
python scripts/recommend_sources.py "我想研究更偏黑帽的SEO对抗思路，并评估可能后果"
```

输出：
- **问题标签** — 自动检测的主题聚类
- **Top 信源** — 按 Relevance × Depth × Actionability × Freshness × Consequence 评分
- **阅读顺序** — 快速执行 → 深度方法论 → 对抗性反例
- **知识缺口** — 建议补充的信源类型
- **24h 实验** — 今天就能跑的一个可执行测试

## Pipeline

这是三阶段内容情报 pipeline 的**第 1 阶段**：

```
edge_source_skill ──→ EdgeKnowledge_Skill ──→ anything-to-md
    (找信源)              (爬取分析)            (转成 MD)
```

| 阶段 | 仓库 | 功能 |
|---|---|---|
| 1 — 找信源 | **edge_source_skill** | 推荐某个主题的高价值信源 |
| 2 — 爬取 | [EdgeKnowledge_Skill](https://github.com/1596941391qq/EdgeKnowledge_Skill) | 深度爬取论坛、Reddit、社区 |
| 3 — 转化 | [anything-to-md](https://github.com/1596941391qq/anything-to-md) | 将任意内容转为 LLM-ready Markdown |

## 数据来源

| 文件 | 内容 |
|---|---|
| `references/karpathy-92-hn-2025.tsv` | Karpathy 筛选的 92 个长文高信号 feed |
| `references/deep-sources-github.tsv` | 扩展后的深水 GitHub 项目（awesome 列表、OSINT 框架、安全工具） |
| `references/deep-sources-telegram.tsv` | Telegram 频道池（可持续导入） |

### 已内置的深水 GitHub 入口

awesome · awesome-osint · OSINT-Framework · awesome-security · awesome-incident-response · papers-we-love · awesome-selfhosted · awesome-sysadmin · awesome-privacy · awesome-threat-detection · awesome-browser-security · awesome-malware-analysis · awesome-devsecops

## 评分公式

```
KnowledgeValue = 0.30×Relevance + 0.25×Depth + 0.25×Actionability + 0.10×Freshness + 0.10×Consequence
```

每个维度 1–5 分，信源按加权 KnowledgeValue 排序。

## Telegram 接入（可选）

```bash
pip install telethon
```

```bash
export TG_API_ID=your_id
export TG_API_HASH=your_hash

python scripts/import_telegram_sources.py --query "seo blackhat osint" --limit 30 --tags "telegram,seo,adversarial"
```

导入的频道自动合并到推荐池。

## 快速开始

```bash
git clone https://github.com/1596941391qq/edge_source_skill.git
cd edge_source_skill
pip install -r requirements.txt  # 或直接运行 — 依赖很少
python scripts/recommend_sources.py "你的研究问题"
```

## 相关项目

- [EdgeKnowledge_Skill](https://github.com/1596941391qq/EdgeKnowledge_Skill) — 第 2 阶段：深度爬取本工具推荐的信源
- [anything-to-md](https://github.com/1596941391qq/anything-to-md) — 第 3 阶段：将爬取内容转为干净 Markdown
- [bypass-anything](https://github.com/1596941391qq/bypass-anything) — 浏览器自动化反检测层
- [nichedigger](https://github.com/1596941391qq/nichedigger) — Reddit 驱动的 PSEO 挖词引擎
