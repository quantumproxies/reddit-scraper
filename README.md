# Reddit Scraper

[![ci](https://github.com/quantumproxies/reddit-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/reddit-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape Reddit from Python or the command line: public posts for a keyword, across Reddit or inside one subreddit, with score, comment count and author, and the full comment tree of any post with depth, parent and timestamps, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there is no Reddit API key to request, no proxy to rotate and no headless browser to keep alive: sign in once and run a command. AI agents can call the same collectors from Claude or any MCP client, and no-code flows from n8n.

```bash
pip install git+https://github.com/quantumproxies/reddit-scraper
reddit-scraper login
reddit-scraper posts "type hints" --subreddit Python --sort top --time year -o posts.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=reddit-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `reddit-scraper posts` | keyword, optional subreddit | Public Reddit posts by search query and/or subreddit, with score and comments, 23 fields per row ([fields and price](https://quanticdata.io/collectors/reddit-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=reddit-scraper)) | up to 250 |
| `reddit-scraper comments` | post URL or id | Author, score, depth, timestamps, 19 fields per row ([fields and price](https://quanticdata.io/collectors/reddit-comments-api/?utm_source=github&utm_medium=readme&utm_campaign=reddit-scraper)) | up to 200 |

`posts` sorts by relevance, top, new or comments and limits the period with `--time` (hour, day, week, month, year or all). `comments` follows the order picked with `--sort`: top, new, controversial, old or qa.

## Sample output

A real row from `reddit-scraper posts "type hints" --subreddit Python --sort top --time year --max-results 3` (2026-10-22):

```json
{
  "id": "t3_1roysjx",
  "url": "https://www.reddit.com/r/Python/comments/1roysjx/pandas_public_api_is_now_typecomplete/",
  "nsfw": false,
  "rank": 2,
  "text": null,
  "flair": null,
  "score": 318,
  "title": "pandas' Public API Is Now Type-Complete",
  "author": "BeamMeUpBiscotti",
  "awards": null,
  "domain": "self.Python",
  "snippet": null,
  "spoiler": false,
  "comments": 35,
  "language": null,
  "author_id": "t2_13i16q",
  "permalink": "https://www.reddit.com/r/Python/comments/1roysjx/pandas_public_api_is_now_typecomplete/",
  "post_type": null,
  "subreddit": "r/Python",
  "thumbnail": null,
  "created_at": "2026-03-09T12:24:57.437Z",
  "subreddit_id": "t5_2qh0y",
  "upvote_ratio": null
}
```

## Python

```python
from quanticdata_reddit_scraper import RedditScraper

reddit = RedditScraper()  # saved login, or QUANTICDATA_API_KEY

posts = reddit.posts("type hints", subreddit="Python", sort="top", time="year", max_results=50)
for p in posts:
    print(p["score"], p["comments"], p["subreddit"], p["title"])

thread = reddit.comments(posts.rows[0]["permalink"], sort="top", max_results=200)
for c in thread:
    print("  " * c["depth"] + f"{c['author']} ({c['score']}): {(c['body'] or '')[:80]}")
thread.to_csv("thread.csv")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Keyword monitor**: Search a few subreddits for the newest posts that mention your keywords and append only the posts not seen before to a JSON Lines file, ready for alerts or a dashboard. See [`examples/subreddit_monitor.py`](examples/subreddit_monitor.py).
- **Comment tree export**: Save the comments of a thread with depth and parent id, as a CSV for a sheet and as an indented text outline to read or to paste into an LLM prompt. See [`examples/comment_tree.py`](examples/comment_tree.py).
- **Top posts by topic**: Find the top posts of the year for a list of keywords, in one subreddit or across Reddit, ranked by score with their comment counts. See [`examples/top_posts.py`](examples/top_posts.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `reddit-scraper run <id> -o out.csv` collects it later.

### `reddit-scraper posts`

Public Reddit posts by search query and/or subreddit, with score and comments.

```
reddit-scraper posts [QUERY] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Keywords to search. Omit to list a subreddit instead. |
| `--subreddit` | string |  | Subreddit name, e.g. "webscraping" (with or without r/). |
| `--sort` | relevance / top / new / hot / rising / comments | `relevance` | Search: relevance \| top \| new \| comments. Listing: hot \| new \| top \| rising. |
| `--time` | hour / day / week / month / year / all | `all` | Restrict to a period (search and top listings). |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `25` | How many posts to deliver at most (1–250). You pay only for delivered posts. |

### `reddit-scraper comments`

The comment tree of any public Reddit post — author, score, depth, timestamps.

```
reddit-scraper comments POST [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `POST` | string |  | Post URL or id, e.g. https://www.reddit.com/r/pics/comments/92dd8/… or 92dd8. |
| `--sort` | top / new / controversial / old / qa | `top` | Comment order (default top). |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `50` | How many comments to deliver at most (1–200). You pay only for delivered comments. |

## Output fields

<details><summary><code>reddit-scraper posts</code>: 23 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position across pages. |
| `id` | string or null | Reddit fullname/id of the post. |
| `title` | string or null | Post title. |
| `subreddit` | string or null | Subreddit (r/name). |
| `author` | string or null | Author username. |
| `score` | integer or null | Net upvotes. |
| `comments` | integer or null | Comment count. |
| `created_at` | string or null | Creation time (ISO 8601). Null on search results — Reddit's search render does not state one. |
| `permalink` | string or null | Post URL on reddit.com. |
| `url` | string or null | What the post links to (self-post = its permalink path). |
| `domain` | string or null | Target domain (self.&lt;sub&gt; for text posts). |
| `nsfw` | boolean | NSFW flag. |
| `flair` | string or null | Post flair when set. |
| `upvote_ratio` | number or null | Share of upvotes, 0–1 (listing rows). |
| `post_type` | string or null | text, link, image, multi_media, video, gif (listing rows). |
| `language` | string or null | Post language (listing rows). |
| `awards` | integer or null | Award count (listing rows). |
| `author_id` | string or null | Author id (t2_…). |
| `subreddit_id` | string or null | Subreddit id (t5_…). |
| `spoiler` | boolean | Marked as spoiler. |
| `text` | string or null | Post body as shown in the feed (listing rows, self posts). |
| `thumbnail` | string or null | Preview image URL. |
| `snippet` | string or null | Search rows: the passage Reddit matched the query on, when Reddit sends one. It does on relevance-sorted searches (the default); a search sorted by top comes back without it, so the field is null there, as on listings. |

</details>

<details><summary><code>reddit-scraper comments</code>: 19 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position in thread order for the chosen sort. |
| `id` | string or null | Comment fullname (t1_…). |
| `parent_id` | string or null | Parent comment fullname; null for top-level comments. |
| `depth` | integer | 0 for top-level, +1 per nesting level. |
| `author` | string or null | Comment author. |
| `body` | string or null | Comment text (markdown rendered to plain text). |
| `score` | integer or null | Net upvotes as shown. |
| `created_at` | string or null | Comment timestamp (ISO 8601). |
| `edited` | boolean | True when the comment was edited. |
| `permalink` | string or null | Direct link to the comment. |
| `is_submitter` | boolean | True when the author is the post's OP. |
| `is_moderator` | boolean | True when the author is a subreddit moderator. |
| `stickied` | boolean | True for pinned comments. |
| `collapsed` | boolean | True when Reddit collapses the comment by default. |
| `author_id` | string or null | Author id (t2_…) when stated. |
| `awards` | integer or null | Award count when stated. |
| `post_id` | string or null | Id of the post the comment belongs to (t3_…). |
| `post_title` | string or null | Title of the post. |
| `subreddit` | string or null | Subreddit of the post (r/…). |

</details>

## Sign-in and API keys

- `reddit-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `reddit-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `reddit-scraper login --api-key`.
- `reddit-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=reddit-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/reddit_posts/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"query": "type hints", "subreddit": "Python", "sort": "top", "time": "year", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=reddit-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=reddit-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Reddit scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a keyword or a post URL and get rows back; the requests run on QuanticData's side. There is no Reddit API key to request either.

**Does it need my Reddit account?**

No. It reads public posts and comments only, the ones anyone can open without signing in. You are responsible for respecting Reddit's terms and the data-protection rules that apply to how you use the data.

**How many results can one run return?**

Up to 250 posts or 200 comments per run; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). Each comment is one row with its depth and parent_id, so the thread can be rebuilt from the sheet.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/subreddit_monitor.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [YouTube Scraper](https://github.com/quantumproxies/youtube-scraper): YouTube scraper for Python and the command line.
- [Instagram Scraper](https://github.com/quantumproxies/instagram-scraper): Instagram scraper for Python and the command line.
- [TikTok Scraper](https://github.com/quantumproxies/tiktok-scraper): TikTok scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=reddit-scraper).
