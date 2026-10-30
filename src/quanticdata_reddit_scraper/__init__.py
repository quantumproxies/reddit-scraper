"""Reddit Scraper: Reddit scraper for Python and the command line: public posts for a keyword, across Reddit or in one subreddit, with score and comment count, and the full comment tree of any post, as JSON or CSV. Free and open source; sign in with your QuanticData account, no Reddit API key, proxies or headless browser to run.

    from quanticdata_reddit_scraper import RedditScraper

    scraper = RedditScraper()   # saved login (`reddit-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.posts(...)   # public Reddit posts for a keyword, optionally in one subreddit
    run = scraper.comments(...)   # the comment tree of one public post
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["RedditScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class RedditScraper:
    """Reddit Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="reddit-scraper/0.1.0 (+https://github.com/quantumproxies/reddit-scraper)", timeout=timeout)

    def posts(
        self, query: Optional[str] = None,
        *,
        subreddit: Optional[str] = None,
        sort: Optional[str] = None,
        time: Optional[str] = None,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Public Reddit posts by search query and/or subreddit, with score and comments.

        Args:
            query: Keywords to search. Omit to list a subreddit instead.
            subreddit: Subreddit name, e.g. "webscraping" (with or without r/).
            sort: Search: relevance | top | new | comments. Listing: hot | new | top | rising. One of: relevance, top, new, hot, rising, comments.
            time: Restrict to a period (search and top listings). One of: hour, day, week, month, year, all.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many posts to deliver at most (1–250). You pay only for delivered posts.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 250 rows, one per post: see ``types.RedditPostsRow``.
        """
        payload = {
            "query": query,
            "subreddit": subreddit,
            "sort": sort,
            "time": time,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("reddit_posts", payload, wait=wait, timeout=timeout)

    def comments(
        self, post: str,
        *,
        sort: Optional[str] = None,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """The comment tree of any public Reddit post — author, score, depth, timestamps.

        Args:
            post: Post URL or id, e.g. https://www.reddit.com/r/pics/comments/92dd8/… or 92dd8.
            sort: Comment order (default top). One of: top, new, controversial, old, qa.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many comments to deliver at most (1–200). You pay only for delivered comments.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 200 rows, one per comment: see ``types.RedditCommentsRow``.
        """
        payload = {
            "post": post,
            "sort": sort,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("reddit_comments", payload, wait=wait, timeout=timeout)
