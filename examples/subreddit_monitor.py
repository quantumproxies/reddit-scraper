"""New Reddit posts that mention your keywords, appended to a JSON Lines file.

Searches each keyword in each subreddit (or across Reddit when no subreddit is
given) for the newest posts and appends only the posts that are not in the
file yet, so every run adds what is new. Run it every hour from cron:

    0 * * * *  cd /path/to/here && python subreddit_monitor.py "type hints" "uv" --subreddits Python learnpython

Needs a login (`reddit-scraper login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import json
import os
from datetime import datetime, timezone

from quanticdata_reddit_scraper import RedditScraper


def seen_ids(path):
    ids = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    ids.add(json.loads(line).get("id"))
    return ids


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("keywords", nargs="+")
    parser.add_argument("--subreddits", nargs="*", default=[], help="subreddit names, with or without r/")
    parser.add_argument("--time", choices=["hour", "day", "week", "month", "year", "all"], default="day")
    parser.add_argument("--max", type=int, default=25, help="posts per keyword and subreddit (max 250)")
    parser.add_argument("--out", default="reddit_mentions.jsonl")
    args = parser.parse_args()

    reddit = RedditScraper()
    seen = seen_ids(args.out)
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    added = 0
    with open(args.out, "a", encoding="utf-8") as fh:
        for subreddit in args.subreddits or [None]:
            for keyword in args.keywords:
                run = reddit.posts(keyword, subreddit=subreddit, sort="new", time=args.time, max_results=args.max)
                fresh = [p for p in run if p.get("id") and p["id"] not in seen]
                for post in fresh:
                    fh.write(json.dumps({"checked_at": checked_at, "keyword": keyword, **post}, ensure_ascii=False) + "\n")
                    seen.add(post["id"])
                    print(f"{post.get('subreddit')} [{keyword}] {post.get('score')} {post.get('title')}")
                added += len(fresh)
    print(f"{added} new posts appended to {args.out}")


if __name__ == "__main__":
    main()
