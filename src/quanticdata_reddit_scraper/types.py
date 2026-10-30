"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class RedditPostsRow(TypedDict, total=False):
    """One row of `reddit-scraper posts` (reddit_posts v2.1.1)."""

    rank: int
    """1-based position across pages."""
    id: Optional[str]
    """Reddit fullname/id of the post."""
    title: Optional[str]
    """Post title."""
    subreddit: Optional[str]
    """Subreddit (r/name)."""
    author: Optional[str]
    """Author username."""
    score: Optional[int]
    """Net upvotes."""
    comments: Optional[int]
    """Comment count."""
    created_at: Optional[str]
    """Creation time (ISO 8601). Null on search results — Reddit's search render does not state one."""
    permalink: Optional[str]
    """Post URL on reddit.com."""
    url: Optional[str]
    """What the post links to (self-post = its permalink path)."""
    domain: Optional[str]
    """Target domain (self.<sub> for text posts)."""
    nsfw: bool
    """NSFW flag."""
    flair: Optional[str]
    """Post flair when set."""
    upvote_ratio: Optional[float]
    """Share of upvotes, 0–1 (listing rows)."""
    post_type: Optional[str]
    """text, link, image, multi_media, video, gif (listing rows)."""
    language: Optional[str]
    """Post language (listing rows)."""
    awards: Optional[int]
    """Award count (listing rows)."""
    author_id: Optional[str]
    """Author id (t2_…)."""
    subreddit_id: Optional[str]
    """Subreddit id (t5_…)."""
    spoiler: bool
    """Marked as spoiler."""
    text: Optional[str]
    """Post body as shown in the feed (listing rows, self posts)."""
    thumbnail: Optional[str]
    """Preview image URL."""
    snippet: Optional[str]
    """Search rows: the passage Reddit matched the query on, when Reddit sends one. It does on relevance-sorted searches (the default); a search sorted by top comes back without it, so the field is null there, as on listings."""

class RedditCommentsRow(TypedDict, total=False):
    """One row of `reddit-scraper comments` (reddit_comments v2.1.2)."""

    rank: int
    """1-based position in thread order for the chosen sort."""
    id: Optional[str]
    """Comment fullname (t1_…)."""
    parent_id: Optional[str]
    """Parent comment fullname; null for top-level comments."""
    depth: int
    """0 for top-level, +1 per nesting level."""
    author: Optional[str]
    """Comment author."""
    body: Optional[str]
    """Comment text (markdown rendered to plain text)."""
    score: Optional[int]
    """Net upvotes as shown."""
    created_at: Optional[str]
    """Comment timestamp (ISO 8601)."""
    edited: bool
    """True when the comment was edited."""
    permalink: Optional[str]
    """Direct link to the comment."""
    is_submitter: bool
    """True when the author is the post's OP."""
    is_moderator: bool
    """True when the author is a subreddit moderator."""
    stickied: bool
    """True for pinned comments."""
    collapsed: bool
    """True when Reddit collapses the comment by default."""
    author_id: Optional[str]
    """Author id (t2_…) when stated."""
    awards: Optional[int]
    """Award count when stated."""
    post_id: Optional[str]
    """Id of the post the comment belongs to (t3_…)."""
    post_title: Optional[str]
    """Title of the post."""
    subreddit: Optional[str]
    """Subreddit of the post (r/…)."""
