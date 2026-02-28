import csv
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KARPATHY = ROOT / "references" / "karpathy-92-hn-2025.tsv"
DEEP_GH = ROOT / "references" / "deep-sources-github.tsv"

QUERY_TAGS = {
    "seo": ["seo", "pseo", "geo", "serp", "排名", "收录", "关键词"],
    "adversarial": ["黑帽", "grey", "gray", "blackhat", "对抗", "绕过", "寄生", "pbn", "bypass"],
    "osint": ["osint", "情报", "intel", "论坛", "leak"],
    "security": ["security", "漏洞", "攻防", "风控", "threat"],
    "research": ["论文", "paper", "research", "methodology"],
    "agent": ["agent", "automation", "workflow", "mcp", "multi-agent"],
    "ecom": ["电商", "shopify", "独立站", "选品", "brand"],
    "ops": ["ops", "运维", "infra", "selfhosted", "自托管", "基础设施"],
    "privacy": ["privacy", "隐私", "匿名", "opsec"],
}

CLUSTER_TAGS = {
    "ai-eng": {"agent", "research"},
    "security": {"security", "adversarial"},
    "systems": {"agent", "research"},
    "policy": {"security", "adversarial"},
    "startup": {"seo", "ecom"},
    "market": {"seo", "ecom"},
    "research": {"research"},
    "eng": {"agent"},
}

CLUSTER_DEPTH = {
    "ai-eng": 4.7,
    "security": 4.6,
    "systems": 4.7,
    "research": 4.6,
    "startup": 4.1,
    "market": 4.0,
    "eng": 4.0,
}

CONSEQUENCE_TEXT = (
    "可能后果: 若直接复制边缘策略而不做沙盒验证，常见后果包括账号/站点风控、排名大幅波动、"
    "品牌信誉受损、投放与人力成本浪费，严重时可能触发法律争议。"
)


@dataclass
class Source:
    name: str
    url: str
    source_type: str
    tags: set[str]
    note: str
    depth: float
    stars: int = 0


def extract_query_tags(query: str) -> set[str]:
    q = query.lower()
    tags = set()
    for tag, kws in QUERY_TAGS.items():
        if any(kw.lower() in q for kw in kws):
            tags.add(tag)
    if not tags:
        tags.add("research")
    return tags


def parse_tags(raw: str) -> set[str]:
    return {x.strip().lower() for x in raw.split(",") if x.strip()}


def load_karpathy_sources() -> list[Source]:
    out = []
    with KARPATHY.open("r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            cluster = row.get("cluster", "")
            tags = set(CLUSTER_TAGS.get(cluster, {"research"}))
            out.append(
                Source(
                    name=row["source_name"],
                    url=row["html_url"],
                    source_type="karpathy",
                    tags=tags,
                    note="长文深度信源，适合建立底层判断和方法论",
                    depth=CLUSTER_DEPTH.get(cluster, 4.0),
                    stars=0,
                )
            )
    return out


def load_deep_github_sources() -> list[Source]:
    out = []
    with DEEP_GH.open("r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            stars = int(row.get("stars", "0"))
            depth = 4.2 + min(0.7, stars / 200000.0)
            out.append(
                Source(
                    name=row["name"],
                    url=row["url"],
                    source_type="deep-github",
                    tags=parse_tags(row.get("tags", "")),
                    note=row.get("note", "深水入口"),
                    depth=round(depth, 2),
                    stars=stars,
                )
            )
    return out


def component_scores(src: Source, qtags: set[str]) -> tuple[float, float, float, float, float]:
    overlap = len(src.tags & qtags)
    relevance = min(5.0, 2.3 + overlap * 1.1)

    depth = src.depth
    freshness = 3.8 if src.source_type == "deep-github" else 3.6

    actionability = 3.5
    if src.source_type == "deep-github":
        actionability = 4.0
        if "workflow" in src.tags or "tools" in src.tags or "meta" in src.tags:
            actionability = 4.4

    consequence = 4.2
    if "adversarial" in qtags:
        consequence = 3.3
        if "adversarial" in src.tags or "security" in src.tags:
            consequence = 3.8

    return relevance, depth, actionability, freshness, consequence


def knowledge_value(scores: tuple[float, float, float, float, float]) -> float:
    r, d, a, f, c = scores
    return round(0.30 * r + 0.25 * d + 0.25 * a + 0.10 * f + 0.10 * c, 2)


def rank_sources(query: str) -> tuple[set[str], list[tuple[float, Source]]]:
    qtags = extract_query_tags(query)
    sources = load_deep_github_sources() + load_karpathy_sources()
    ranked = []
    for src in sources:
        kv = knowledge_value(component_scores(src, qtags))
        ranked.append((kv, src))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return qtags, ranked


def diversified_top(ranked: list[tuple[float, Source]], n: int = 10) -> list[tuple[float, Source]]:
    chosen = []
    karpathy_count = 0
    deep_count = 0
    for kv, src in ranked:
        if len(chosen) >= n:
            break
        if src.source_type == "deep-github" and deep_count < 5:
            chosen.append((kv, src))
            deep_count += 1
        elif src.source_type == "karpathy" and karpathy_count < 5:
            chosen.append((kv, src))
            karpathy_count += 1
    return chosen


def missing_list_types(qtags: set[str], top: list[tuple[float, Source]]) -> list[str]:
    covered = set()
    for _, src in top:
        covered |= src.tags

    needs = []
    if "adversarial" in qtags and "platform-policy-changelog" not in covered:
        needs.append("平台政策/处罚案例变更列表（用于判断策略时效）")
    if "seo" in qtags and "seo-forum-index" not in covered:
        needs.append("SEO 实战论坛索引列表（白灰黑对抗样本）")
    if "osint" in qtags and "regional-forums" not in covered:
        needs.append("区域化语言论坛入口列表（俄语/西语/阿语）")
    if "security" in qtags and "legal-casebook" not in covered:
        needs.append("合规与执法判例索引列表（用于后果评估）")
    if "ecom" in qtags and "ad-network-abuse" not in covered:
        needs.append("广告平台风控与封禁案例列表（投放对抗视角）")
    if not needs:
        needs.append("私域高质量社区列表（付费论坛/邀请码社群）的可验证目录")
    return needs


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/recommend_sources.py '<question>'")
        return 1

    question = sys.argv[1]
    qtags, ranked = rank_sources(question)
    deep_count = len(load_deep_github_sources())
    top = diversified_top(ranked, n=10)

    print(f"问题标签: {','.join(sorted(qtags))}")
    print(f"候选库: Karpathy 92 + Deep GitHub {deep_count}")
    print("推荐信源 Top 10:")
    for i, (kv, src) in enumerate(top, 1):
        star_text = f" | stars {src.stars}" if src.stars else ""
        print(f"{i}. {src.name} ({src.source_type}){star_text} | KnowledgeValue {kv}/5 | {src.note} | {src.url}")

    print("优先阅读顺序: 2个可执行入口 -> 2个方法论深读 -> 1个对抗反例校准")
    if "adversarial" in qtags or "seo" in qtags:
        print(CONSEQUENCE_TEXT)
    print("建议补充列表类型:")
    for item in missing_list_types(qtags, top):
        print(f"- {item}")
    print("实验建议: 24小时内用前3个信源产出一页策略卡，包含目标、假设、最小实验和止损条件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
