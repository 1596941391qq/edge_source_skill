import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
KARPATHY = ROOT / "references" / "karpathy-92-hn-2025.tsv"
LOCAL = ROOT / "references" / "local-89-links.txt"

PROJECT_KEYWORDS = {
    "AI陪伴与真人感交互": ["陪伴", "角色", "persona", "chat", "conversation", "emotion"],
    "记忆系统（短中长期）": ["memory", "mem0", "memobase", "retrieval", "记忆", "向量"],
    "模型选型与路由": ["model", "route", "router", "gemini", "claude", "gpt", "deepseek"],
    "PSEO/SEO/GEO增长引擎": ["seo", "pseo", "geo", "serp", "关键词", "收录", "排名", "pbn"],
    "Agent自动化与工具栈": ["agent", "workflow", "api", "automation", "n8n", "tool"],
    "商业化与交付SOP": ["sop", "商业", "报价", "客户", "交付", "b2b"],
}

QUERY_TAGS = {
    "seo": ["seo", "pseo", "geo", "serp", "收录", "排名", "关键词"],
    "risk": ["风险", "合规", "policy", "risk", "黑帽", "blackhat", "pbn", "寄生", "bypass"],
    "agent": ["agent", "workflow", "automation", "tool", "multi-agent", "mcp"],
    "memory": ["memory", "mem0", "memobase", "记忆", "retrieval"],
    "ecom": ["跨境", "电商", "shopify", "独立站", "选品"],
    "social": ["xhs", "小红书", "instagram", "multiaccount", "账号矩阵", "reddit", "x.com"],
    "adult": ["adult", "sex", "toys", "情趣", "成人", "nsfw"],
}

CLUSTER_TAGS = {
    "ai-eng": {"agent", "memory"},
    "security": {"risk"},
    "systems": {"agent"},
    "policy": {"risk"},
    "startup": {"seo", "ecom"},
    "market": {"seo", "ecom"},
    "tools": {"agent"},
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

DOMAIN_HINTS = {
    "github.com": ("开源实现和代码结构，适合快速落地 PoC", {"agent", "memory"}),
    "shopify.dev": ("官方平台文档，适合落地电商工作流", {"ecom", "agent"}),
    "reddit.com": ("真实案例和失败样本，适合提炼反例与坑点", {"seo", "social", "risk"}),
    "blackhatworld.com": ("灰黑策略样本库，可用于风险边界识别", {"risk", "seo"}),
    "bestblackhatforum.com": ("高风险论坛信息，建议仅作风险研究", {"risk", "seo"}),
    "domainhuntergatherer.com": ("PBN路线知识，适合做政策红线对照", {"risk", "seo"}),
    "llmstxt.org": ("LLM可发现性提案，适合AI可见性实验", {"seo", "agent"}),
    "skills.sh": ("Agent 技能市场参考，适合工具链选型", {"agent"}),
    "onehack.st": ("边缘玩法样本，适合反例验证和风险建模", {"risk", "seo", "social"}),
    "x.com": ("一线从业者动态，适合捕捉最新信号", {"social", "seo"}),
    "nstbrowser.io": ("多账号浏览器能力信息，适合社媒矩阵工具调研", {"social"}),
    "talents-ai.com": ("人才和岗位信号，适合商业化交付能力建设", {"ecom"}),
    "lelo.com": ("垂直品类品牌样本，适合成人品类竞品分析", {"adult", "ecom"}),
    "smilemakerscollection.com": ("品牌内容策略样本，适合成人品类定位", {"adult", "ecom"}),
    "dame.com": ("品牌和产品叙事样本，适合高客单策略研究", {"adult", "ecom"}),
}


@dataclass
class Source:
    name: str
    url: str
    source_type: str
    tags: set[str]
    note: str
    cluster: str = ""


def detect_project(query: str) -> str:
    q = query.lower()
    best_name, best_score = "Agent自动化与工具栈", 0
    for name, kws in PROJECT_KEYWORDS.items():
        score = sum(1 for kw in kws if kw.lower() in q)
        if score > best_score:
            best_name, best_score = name, score
    return best_name


def extract_query_tags(query: str) -> set[str]:
    q = query.lower()
    tags = set()
    for tag, kws in QUERY_TAGS.items():
        if any(kw.lower() in q for kw in kws):
            tags.add(tag)
    return tags


def local_source_from_url(url: str) -> Source:
    parsed = urlparse(url)
    host = parsed.netloc.lower().replace("www.", "")
    name = host or url
    note = "一线实战线索，可用于验证假设"
    tags = {"agent"}
    for domain, (hint, dtags) in DOMAIN_HINTS.items():
        if domain in host:
            note = hint
            tags = set(dtags)
            break
    if "feishu.cn" in host or "qq.com" in host or "meeting.tencent.com" in host:
        note = "内部协作线索，适合回溯原始上下文"
        tags = {"agent"}
    if "gemini.google.com" in host or "chatgpt.com" in host:
        note = "模型实测样本，适合提炼提示词与任务编排"
        tags = {"agent", "memory"}
    return Source(name=name, url=url, source_type="local", tags=tags, note=note)


def load_karpathy_sources() -> list[Source]:
    out = []
    with KARPATHY.open("r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            cluster = row.get("cluster", "")
            tags = set(CLUSTER_TAGS.get(cluster, {"agent"}))
            out.append(
                Source(
                    name=row["source_name"],
                    url=row["html_url"],
                    source_type="karpathy",
                    tags=tags,
                    note="长文深度信源，适合建立方法论和技术判断",
                    cluster=cluster,
                )
            )
    return out


def load_local_sources() -> list[Source]:
    out = []
    with LOCAL.open("r", encoding="utf-8-sig") as f:
        for line in f:
            url = line.strip()
            if url.startswith("http"):
                out.append(local_source_from_url(url))
    return out


def component_scores(src: Source, qtags: set[str]) -> tuple[float, float, float, float, float]:
    overlap = len(src.tags & qtags)
    relevance = min(5.0, 2.2 + overlap * 1.2)

    if src.source_type == "karpathy":
        depth = CLUSTER_DEPTH.get(src.cluster, 4.0)
        actionability = 3.8 if src.cluster in {"ai-eng", "systems", "eng", "tools"} else 3.3
        freshness = 3.6
    else:
        depth = 3.5
        actionability = 3.4
        freshness = 4.0
        if "github.com" in src.url or "shopify.dev" in src.url:
            depth = 4.2
            actionability = 4.6
        if "reddit.com" in src.url or "x.com" in src.url:
            depth = 3.3
            freshness = 4.3

    risk = 4.2
    risky = "risk" in src.tags
    if risky and "risk" not in qtags:
        risk = 1.6
    elif risky and "risk" in qtags:
        risk = 3.2

    return relevance, depth, actionability, freshness, risk


def knowledge_value(scores: tuple[float, float, float, float, float]) -> float:
    r, d, a, f, k = scores
    return round(0.30 * r + 0.25 * d + 0.25 * a + 0.10 * f + 0.10 * k, 2)


def rank_sources(query: str) -> list[tuple[float, float, Source]]:
    qtags = extract_query_tags(query)
    sources = load_karpathy_sources() + load_local_sources()
    ranked = []
    for src in sources:
        scores = component_scores(src, qtags)
        kv = knowledge_value(scores)
        rel = scores[0]
        ranked.append((kv, rel, src))
    ranked.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return ranked


def diversified_top(ranked: list[tuple[float, float, Source]], n: int = 10) -> list[tuple[float, float, Source]]:
    top = ranked[: n * 4]
    chosen = []
    local_picked = 0
    host_count = {}
    for item in top:
        if len(chosen) >= n:
            break
        _, rel, src = item
        host = urlparse(src.url).netloc.lower().replace("www.", "")
        if host_count.get(host, 0) >= 2:
            continue
        if src.source_type == "local" and rel >= 3.4:
            chosen.append(item)
            local_picked += 1
            host_count[host] = host_count.get(host, 0) + 1
        elif src.source_type == "karpathy":
            chosen.append(item)
            host_count[host] = host_count.get(host, 0) + 1

    if local_picked < 2:
        for item in top:
            if len(chosen) >= n:
                break
            if item in chosen:
                continue
            _, rel, src = item
            host = urlparse(src.url).netloc.lower().replace("www.", "")
            if host_count.get(host, 0) >= 2:
                continue
            if src.source_type == "local" and rel >= 2.2:
                chosen.append(item)
                local_picked += 1
                host_count[host] = host_count.get(host, 0) + 1
                if local_picked >= 2:
                    break

    return chosen[:n]


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/recommend_sources.py '<question>'")
        return 1

    question = sys.argv[1]
    project = detect_project(question)
    qtags = extract_query_tags(question)
    ranked = rank_sources(question)
    top = diversified_top(ranked, n=10)
    local_count = len(load_local_sources())

    print(f"问题归类: {project}")
    print(f"问题标签: {','.join(sorted(qtags)) if qtags else 'general'}")
    print(f"候选库: Karpathy 92 + Local {local_count}")
    print("推荐信源 Top 10:")
    for i, (kv, _, src) in enumerate(top, 1):
        print(f"{i}. {src.name} ({src.source_type}) | KnowledgeValue {kv}/5 | {src.note} | {src.url}")

    if "risk" in qtags:
        print("风险提示: 已包含高风险样本源，建议仅用于风险边界研究，不直接复制执行。")

    print("优先阅读顺序: 2个可执行文档/代码 -> 2个深度方法论 -> 1个反例与风险校验")
    print("实验建议: 24小时内根据前3条信源输出SOP草案，并定义收录率/转化率/违规率3个指标")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
