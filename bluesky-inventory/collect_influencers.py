#!/usr/bin/env python3
"""Bluesky influencer inventory collector.

Read-only, UNAUTHENTICATED, against https://public.api.bsky.app/xrpc only.
No login, no app password, no agent account, and no write of any kind
(no follow/like/post/reply/DM). It reads the public appview and writes one CSV.

Built to knick's step-1 plan for the "Bluesky influencer inventory" work-queue
entry. "hot" == reach and engagement only: follower count, posting cadence,
likes per post. No appearance is read or recorded, and gender is recorded only
when self-declared in pronouns/bio, otherwise left empty.

Idempotent: re-running overwrites the output CSV, dedups by DID, and orders
rows deterministically (niche, then followers descending, then handle). The
underlying network data drifts between runs; the script's behaviour does not.
"""

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE = "https://public.api.bsky.app/xrpc"
FOLLOWER_FLOOR = 10_000
DORMANT_DAYS = 90
AUTHORFEED_SAMPLE = 30

NICHE_SEEDS = {
    "Tech": ["developer", "software engineer", "open source", "programming"],
    "AI/ML": ["machine learning", "AI researcher", "LLM", "data science"],
    "Science": ["scientist", "astronomy", "biology", "science communicator"],
    "Journalism": ["journalist", "reporter", "correspondent", "columnist"],
    "Politics": ["political analyst", "policy analyst", "political commentator", "politics"],
    "Books": ["author", "novelist", "writer", "poet"],
    "Art": ["artist", "illustrator", "painter", "digital art"],
    "Games": ["game developer", "indie games", "gamer", "game design"],
    "Sports": ["sports journalist", "athlete", "sports writer", "coach"],
    "Music": ["musician", "songwriter", "music producer", "composer"],
    "Film/TV": ["filmmaker", "director", "screenwriter", "actor"],
    "Finance": ["economist", "investor", "finance", "trader"],
}

FEED_NICHE_KEYWORDS = {
    "Tech": ["tech", "programming", "developer", "coding", "software", "linux", "web dev"],
    "AI/ML": ["ai", "machine learning", "data science", "llm"],
    "Science": ["science", "astronomy", "space", "biology", "physics", "climate", "nature"],
    "Journalism": ["news", "journalism", "media", "press"],
    "Politics": ["politics", "political", "policy"],
    "Books": ["book", "reading", "author", "literature", "writers"],
    "Art": ["art", "illustration", "design", "artists", "comics"],
    "Games": ["game", "gaming", "gamedev"],
    "Sports": ["sport", "football", "soccer", "nba", "basketball", "baseball", "hockey"],
    "Music": ["music", "songs", "band"],
    "Film/TV": ["film", "movie", "cinema", "tv", "television"],
    "Finance": ["finance", "economics", "markets", "investing", "crypto", "money"],
}

PRONOUN_RE = re.compile(
    r"\b("
    r"she\s*/\s*her(?:\s*/\s*hers)?|"
    r"he\s*/\s*him(?:\s*/\s*his)?|"
    r"they\s*/\s*them(?:\s*/\s*theirs)?|"
    r"she\s*/\s*they|he\s*/\s*they|they\s*/\s*she|they\s*/\s*he|"
    r"ze\s*/\s*(?:zir|hir)|xe\s*/\s*xem|fae\s*/\s*faer|"
    r"any\s+pronouns|all\s+pronouns"
    r")\b",
    re.IGNORECASE,
)

PARODY_RE = re.compile(
    r"\b(parody|satire|fan\s*account|fanpage|not\s+affiliated|impersonat|"
    r"tribute\s+account|unofficial|fake\b)",
    re.IGNORECASE,
)

BOT_RE = re.compile(
    r"\b(automated\s+account|this\s+is\s+a\s+bot|bot\s+account|"
    r"posts?\s+automatically|🤖\s*bot)\b",
    re.IGNORECASE,
)

ORG_RE = re.compile(
    r"\b(official\s+account\s+of|we\s+are\s+a|our\s+mission|"
    r"©|\bLLC\b|\bInc\.|\bGmbH\b|\bLtd\b|subscribe\s+to\s+our|"
    r"follow\s+for\s+the\s+latest|brought\s+to\s+you\s+by)\b",
    re.IGNORECASE,
)


class Client:
    def __init__(self, sleep=0.25, verbose=False):
        self.sleep = sleep
        self.verbose = verbose
        self.calls = 0

    def _log(self, *a):
        if self.verbose:
            print(*a, file=sys.stderr)

    def get(self, method, params, retries=4):
        url = f"{BASE}/{method}?{urllib.parse.urlencode(params, doseq=True)}"
        for attempt in range(retries):
            req = urllib.request.Request(
                url, headers={"User-Agent": "knack-oikos-bsky-inventory/1.0"}
            )
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    self.calls += 1
                    self._respect_ratelimit(resp.headers)
                    time.sleep(self.sleep)
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    wait = int(e.headers.get("retry-after", "0") or "0") or (2 ** attempt) * 5
                    self._log(f"[429] {method} backing off {wait}s")
                    time.sleep(wait)
                    continue
                if e.code in (502, 503, 504):
                    time.sleep((2 ** attempt) * 2)
                    continue
                self._log(f"[HTTP {e.code}] {method} {params}")
                return None
            except (urllib.error.URLError, TimeoutError) as e:
                self._log(f"[net] {method}: {e}; retry")
                time.sleep((2 ** attempt) * 2)
        return None

    def _respect_ratelimit(self, headers):
        remaining = headers.get("ratelimit-remaining")
        reset = headers.get("ratelimit-reset")
        if remaining is None:
            return
        try:
            remaining = int(remaining)
        except ValueError:
            return
        if remaining <= 2 and reset:
            try:
                pause = max(0, int(reset) - int(time.time())) + 1
                self._log(f"[ratelimit] {remaining} left; sleeping {pause}s to reset")
                time.sleep(min(pause, 60))
            except ValueError:
                pass


def paged(client, method, params, key, max_pages):
    out = []
    cursor = None
    for _ in range(max_pages):
        p = dict(params)
        if cursor:
            p["cursor"] = cursor
        data = client.get(method, p)
        if not data:
            break
        items = data.get(key, [])
        out.extend(items)
        cursor = data.get("cursor")
        if not cursor or not items:
            break
    return out


def discover_search(client, candidates, args):
    for niche, terms in NICHE_SEEDS.items():
        for term in terms:
            actors = paged(
                client, "app.bsky.actor.searchActors",
                {"term": term, "limit": 100}, "actors", args.search_pages,
            )
            for a in actors:
                add_candidate(candidates, a["did"], a.get("handle"),
                              niche, f"search:{niche}:{term}")
            client._log(f"[search] {niche}/{term}: {len(actors)} actors")


def discover_trending(client, candidates, args):
    data = client.get("app.bsky.unspecced.getTrendingTopics", {"limit": 25})
    if not data:
        return
    for t in data.get("topics", []):
        term = t.get("topic") or t.get("displayName")
        if not term:
            continue
        actors = paged(
            client, "app.bsky.actor.searchActors",
            {"term": term, "limit": 50}, "actors", 1,
        )
        for a in actors:
            add_candidate(candidates, a["did"], a.get("handle"),
                          "Trending", f"trending:{term}")


def match_feed_niche(name):
    low = name.lower()
    for niche, kws in FEED_NICHE_KEYWORDS.items():
        if any(kw in low for kw in kws):
            return niche
    return None


def discover_feeds(client, candidates, args):
    data = client.get("app.bsky.unspecced.getPopularFeedGenerators", {"limit": 100})
    feeds = data.get("feeds", []) if data else []

    always = {
        "at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.generator/whats-hot": ("General", "feed:whats-hot"),
        "at://did:plc:3guzzweuqraryl3rdkimjamk/app.bsky.feed.generator/for-you": ("General", "feed:for-you"),
    }
    walk = dict(always)
    for f in feeds:
        niche = match_feed_niche(f.get("displayName", ""))
        if niche and f["uri"] not in walk:
            walk[f["uri"]] = (niche, f"feed:{f.get('displayName')}")
        if len(walk) >= args.max_feeds:
            break

    for uri, (niche, source) in walk.items():
        items = paged(
            client, "app.bsky.feed.getFeed",
            {"feed": uri, "limit": 100}, "feed", args.feed_pages,
        )
        for it in items:
            author = it.get("post", {}).get("author", {})
            if author.get("did"):
                add_candidate(candidates, author["did"], author.get("handle"),
                              niche, source)
        client._log(f"[feed] {source}: {len(items)} posts")


def add_candidate(candidates, did, handle, niche, source):
    c = candidates.setdefault(did, {"handle": handle, "niches": [], "sources": []})
    if niche not in c["niches"]:
        c["niches"].append(niche)
    if source not in c["sources"]:
        c["sources"].append(source)


def primary_niche(niches):
    """Prefer one of the 12 target niches over the Trending/General discovery
    buckets, so a person found in both a niche search and a trending topic is
    filed under the niche."""
    for n in niches:
        if n in NICHE_SEEDS:
            return n
    for n in niches:
        if n not in ("General",):
            return n
    return niches[0] if niches else "General"


def hydrate(client, dids):
    profiles = {}
    for i in range(0, len(dids), 25):
        batch = dids[i:i + 25]
        data = client.get("app.bsky.actor.getProfiles", {"actors": batch})
        if not data:
            continue
        for p in data.get("profiles", []):
            profiles[p["did"]] = p
    return profiles


def account_age_days(created_at):
    if not created_at:
        return None
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).days
    except ValueError:
        return None


def author_metrics(client, did):
    data = client.get(
        "app.bsky.feed.getAuthorFeed",
        {"actor": did, "limit": AUTHORFEED_SAMPLE, "filter": "posts_no_replies"},
    )
    if not data:
        return None
    posts = []
    for it in data.get("feed", []):
        post = it.get("post", {})
        # Skip reposts by this author of others' content for the cadence math.
        if it.get("reason", {}).get("$type", "").endswith("reasonRepost"):
            continue
        rec = post.get("record", {})
        indexed = post.get("indexedAt") or rec.get("createdAt")
        posts.append({
            "indexedAt": indexed,
            "likes": post.get("likeCount", 0) or 0,
            "reposts": post.get("repostCount", 0) or 0,
        })
    if not posts:
        return {"posts_per_week": 0.0, "likes_per_post": 0.0,
                "last_post_days": None, "sampled": 0, "viral": False}

    times = []
    for p in posts:
        try:
            times.append(datetime.fromisoformat(p["indexedAt"].replace("Z", "+00:00")))
        except (ValueError, AttributeError):
            pass
    last_post_days = None
    posts_per_week = 0.0
    if times:
        newest, oldest = max(times), min(times)
        last_post_days = (datetime.now(timezone.utc) - newest).days
        span_weeks = max((newest - oldest).total_seconds() / (7 * 86400), 1e-9)
        posts_per_week = round(len(times) / span_weeks, 2) if len(times) > 1 else float(len(times))

    likes = [p["likes"] for p in posts]
    likes_per_post = round(sum(likes) / len(likes), 1)
    median = sorted(likes)[len(likes) // 2]
    viral = bool(median >= 0 and max(likes) > 20 * max(median, 1) and max(likes) > 500)

    return {
        "posts_per_week": posts_per_week,
        "likes_per_post": likes_per_post,
        "last_post_days": last_post_days,
        "sampled": len(posts),
        "viral": viral,
    }


def self_declared_pronouns(text):
    if not text:
        return ""
    m = PRONOUN_RE.search(text)
    return re.sub(r"\s+", "", m.group(1)).lower() if m else ""


def classify(profile, metrics):
    """Return (drop_reason or None, flags list). Keep-and-flag beats dropping
    for borderline signals; only hard disqualifiers drop a row."""
    name = profile.get("displayName", "") or ""
    bio = profile.get("description", "") or ""
    handle = profile.get("handle", "") or ""
    blob = f"{name} {bio} {handle}"
    flags = []

    if PARODY_RE.search(blob):
        return "parody/fan/impersonation", flags
    if BOT_RE.search(blob) or handle.lower().endswith("bot.bsky.social"):
        return "bot", flags
    if ORG_RE.search(blob):
        return "institutional/brand/org", flags

    if metrics is None:
        return "no-author-feed", flags
    if metrics["last_post_days"] is not None and metrics["last_post_days"] > DORMANT_DAYS:
        return f"dormant>{DORMANT_DAYS}d", flags

    followers = profile.get("followersCount", 0) or 0
    following = profile.get("followsCount", 0) or 0
    lpp = metrics["likes_per_post"]

    if followers > 0 and following > 2 * followers and following > 5000:
        flags.append("high-follow-ratio")
    if followers >= 50_000 and lpp < followers * 0.0002:
        flags.append("low-engagement-for-reach")
    if metrics["viral"]:
        flags.append("viral-inflation")
    if metrics["sampled"] < 5:
        flags.append("thin-sample")
    if any("official" in b.lower() for b in [name, bio]):
        flags.append("possible-org")

    return None, flags


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="bluesky_influencers.csv")
    ap.add_argument("--sleep", type=float, default=0.25, help="seconds between API calls")
    ap.add_argument("--search-pages", type=int, default=1, help="searchActors pages per term")
    ap.add_argument("--feed-pages", type=int, default=2, help="getFeed pages per generator")
    ap.add_argument("--max-feeds", type=int, default=14, help="cap on feed generators walked")
    ap.add_argument("--max-authorfeed", type=int, default=500,
                    help="cap on getAuthorFeed calls (the rate-limit bottleneck)")
    ap.add_argument("--per-niche", type=int, default=25,
                    help="max rows kept per target niche (balances coverage)")
    ap.add_argument("--overflow-cap", type=int, default=12,
                    help="max rows from the Trending/General discovery buckets")
    ap.add_argument("--no-feeds", action="store_true", help="skip feed-generator discovery")
    ap.add_argument("--no-trending", action="store_true", help="skip trending-topic seeds")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    client = Client(sleep=args.sleep, verbose=args.verbose)
    candidates = {}

    print("[1/4] search discovery...", file=sys.stderr)
    discover_search(client, candidates, args)
    if not args.no_trending:
        print("[2/4] trending-topic seeds...", file=sys.stderr)
        discover_trending(client, candidates, args)
    if not args.no_feeds:
        print("[3/4] feed-generator discovery...", file=sys.stderr)
        discover_feeds(client, candidates, args)

    print(f"      {len(candidates)} unique candidate DIDs; hydrating...", file=sys.stderr)
    profiles = hydrate(client, list(candidates.keys()))

    over_floor = [
        did for did, p in profiles.items()
        if (p.get("followersCount", 0) or 0) >= FOLLOWER_FLOOR
    ]
    print(f"      {len(over_floor)} candidates over the {FOLLOWER_FLOOR:,} floor",
          file=sys.stderr)

    buckets = {}
    for did in over_floor:
        niche = primary_niche(candidates[did]["niches"])
        buckets.setdefault(niche, []).append(did)
    for niche in buckets:
        buckets[niche].sort(key=lambda d: -(profiles[d].get("followersCount", 0) or 0))

    selection = []
    for niche in list(NICHE_SEEDS) + ["Trending", "General"]:
        cap = args.per_niche if niche in NICHE_SEEDS else args.overflow_cap
        selection.extend(buckets.get(niche, [])[:cap])
    print(f"      selected {len(selection)} across {len(buckets)} buckets "
          f"(cap {args.per_niche}/niche)", file=sys.stderr)

    print("[4/4] author-feed metrics + classification...", file=sys.stderr)
    rows = []
    reasons = {}
    af_calls = 0
    for did in selection:
        if af_calls >= args.max_authorfeed:
            break
        p = profiles[did]
        metrics = author_metrics(client, did)
        af_calls += 1
        drop, flags = classify(p, metrics)
        if drop:
            reasons[drop] = reasons.get(drop, 0) + 1
            continue
        cand = candidates[did]
        niche = primary_niche(cand["niches"])
        bio = p.get("description", "") or ""
        rows.append({
            "handle": p.get("handle", ""),
            "did": did,
            "display_name": p.get("displayName", "") or "",
            "followers": p.get("followersCount", 0) or 0,
            "following": p.get("followsCount", 0) or 0,
            "posts": p.get("postsCount", 0) or 0,
            "account_age_days": account_age_days(p.get("createdAt")) or "",
            "bio": bio,
            "self_declared_pronouns_gender": self_declared_pronouns(f"{p.get('displayName','')} {bio}"),
            "niche": niche,
            "posts_per_week": metrics["posts_per_week"],
            "likes_per_post": metrics["likes_per_post"],
            "source": "; ".join(cand["sources"]),
            "flags": "; ".join(flags),
        })

    rows.sort(key=lambda r: (r["niche"], -r["followers"], r["handle"]))

    fields = ["handle", "did", "display_name", "followers", "following", "posts",
              "account_age_days", "bio", "self_declared_pronouns_gender", "niche",
              "posts_per_week", "likes_per_post", "source", "flags"]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    by_niche = {}
    for r in rows:
        by_niche[r["niche"]] = by_niche.get(r["niche"], 0) + 1
    print(f"\nWrote {len(rows)} rows to {args.out}", file=sys.stderr)
    print(f"API calls: {client.calls} (author-feed: {af_calls})", file=sys.stderr)
    print(f"Rows by niche: {json.dumps(by_niche, sort_keys=True)}", file=sys.stderr)
    print(f"Dropped by reason: {json.dumps(reasons, sort_keys=True)}", file=sys.stderr)


if __name__ == "__main__":
    main()
