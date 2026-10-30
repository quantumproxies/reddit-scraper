"""The top Reddit posts for a list of keywords, ranked by score.

    python top_posts.py "type hints" "asyncio" "packaging" --subreddit Python --time year --top 25

Writes top_posts.csv with every post and the keyword that found it (a post
found by two keywords is kept once), then prints the ten posts with the
highest score and their comment counts.
"""

import argparse

from quanticdata_reddit_scraper import RedditScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("keywords", nargs="+")
    parser.add_argument("--subreddit", help="limit the search to one subreddit")
    parser.add_argument("--time", choices=["hour", "day", "week", "month", "year", "all"], default="year")
    parser.add_argument("--top", type=int, default=25, help="posts per keyword (max 250)")
    parser.add_argument("--out", default="top_posts.csv")
    args = parser.parse_args()

    reddit = RedditScraper()
    posts = {}
    for keyword in args.keywords:
        run = reddit.posts(keyword, subreddit=args.subreddit, sort="top", time=args.time, max_results=args.top)
        print(f"{keyword!r}: {len(run)} posts")
        for post in run:
            posts.setdefault(post.get("id") or post.get("permalink"), {"keyword": keyword, **post})

    rows = sorted(posts.values(), key=lambda p: p.get("score") or 0, reverse=True)
    write(rows, args.out)
    print(f"{len(rows)} unique posts written to {args.out}")
    for post in rows[:10]:
        print(f"  {post.get('score') or 0:6d} points  {post.get('comments') or 0:5d} comments  "
              f"{post.get('subreddit')}  {post.get('title')}")


if __name__ == "__main__":
    main()
