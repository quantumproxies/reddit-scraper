"""Export the comment tree of a Reddit post, as CSV and as an indented outline.

    python comment_tree.py https://www.reddit.com/r/Python/comments/1roysjx/pandas_public_api_is_now_typecomplete/ --max 200

Writes thread.csv (one row per comment, with depth and parent_id) and
thread.txt, the same thread as an indented text outline in page order, easy to
read, to paste into a document or to give to an LLM as context.
"""

import argparse

from quanticdata_reddit_scraper import RedditScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("post", help="post URL or id")
    parser.add_argument("--sort", choices=["top", "new", "controversial", "old", "qa"], default="top")
    parser.add_argument("--max", type=int, default=200, help="comments to deliver (max 200)")
    parser.add_argument("--out", default="thread", help="file name without extension")
    args = parser.parse_args()

    reddit = RedditScraper()
    run = reddit.comments(args.post, sort=args.sort, max_results=args.max)
    write(run, args.out + ".csv")

    with open(args.out + ".txt", "w", encoding="utf-8") as fh:
        if run.rows:
            first = run.rows[0]
            fh.write(f"{first.get('post_title')} ({first.get('subreddit')})\n\n")
        for comment in run:
            indent = "    " * (comment.get("depth") or 0)
            body = " ".join((comment.get("body") or "").split())
            fh.write(f"{indent}{comment.get('author')} ({comment.get('score')} points, {comment.get('created_at')}):\n")
            fh.write(f"{indent}{body}\n\n")

    top_level = sum(1 for c in run if not c.get("parent_id"))
    print(f"{len(run)} comments ({top_level} top-level) written to {args.out}.csv and {args.out}.txt")


if __name__ == "__main__":
    main()
