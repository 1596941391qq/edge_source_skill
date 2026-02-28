import argparse
import csv
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "references" / "deep-sources-telegram.tsv"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Import Telegram channels into deep-sources-telegram.tsv via Telethon search."
    )
    p.add_argument("--query", required=True, help="Search keywords, e.g. 'seo blackhat osint'")
    p.add_argument("--limit", type=int, default=30, help="Max channels to store")
    p.add_argument(
        "--tags",
        default="telegram,adversarial",
        help="Comma-separated tags to assign to imported channels",
    )
    return p.parse_args()


def ensure_header(path: Path) -> None:
    if path.exists():
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["name", "type", "members", "tags", "url", "note", "last_seen_utc"])


def load_existing_urls(path: Path) -> set[str]:
    urls = set()
    if not path.exists():
        return urls
    with path.open("r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            url = (row.get("url") or "").strip()
            if url:
                urls.add(url)
    return urls


async def search_and_append(query: str, limit: int, tags: str) -> int:
    try:
        from telethon import TelegramClient
        from telethon import functions
        from telethon.tl.types import Channel
    except Exception as e:  # pragma: no cover
        raise SystemExit(
            "Telethon is required. Install with: pip install telethon\n"
            f"Import error: {e}"
        )

    api_id = os.getenv("TG_API_ID")
    api_hash = os.getenv("TG_API_HASH")
    session = os.getenv("TG_SESSION", "edge_source_skill")
    if not api_id or not api_hash:
        raise SystemExit("Missing TG_API_ID / TG_API_HASH env vars.")

    ensure_header(OUT)
    existing = load_existing_urls(OUT)
    rows = []

    async with TelegramClient(session, int(api_id), api_hash) as client:
        # This uses Telegram global entity search from user account context.
        result = await client(functions.contacts.SearchRequest(q=query, limit=limit))
        for chat in result.chats:
            if not isinstance(chat, Channel):
                continue
            username = getattr(chat, "username", None)
            if not username:
                continue
            url = f"https://t.me/{username}"
            if url in existing:
                continue
            title = getattr(chat, "title", username)
            members = getattr(chat, "participants_count", 0) or 0
            rows.append(
                {
                    "name": title,
                    "type": "telegram",
                    "members": str(members),
                    "tags": tags,
                    "url": url,
                    "note": f"Telegram 搜索导入: {query}",
                    "last_seen_utc": "2026-02-28T00:00:00Z",
                }
            )

    if not rows:
        return 0

    with OUT.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "type", "members", "tags", "url", "note", "last_seen_utc"],
            delimiter="\t",
        )
        for row in rows:
            writer.writerow(row)
    return len(rows)


def main() -> int:
    args = parse_args()
    import asyncio

    count = asyncio.run(search_and_append(args.query, args.limit, args.tags))
    print(f"Imported {count} Telegram sources into {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
