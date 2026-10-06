"""Post a review to GitHub. Only ever called when the user passes --post.

NOTE: docs.github.com was not reachable while building this, so the request
shape (POST /repos/{o}/{r}/pulls/{n}/reviews with body/event/comments[path,
line,side]) comes from the author's memory of the REST API and has NOT been
verified against the docs or a live PR. Check it before trusting --post.
"""
from __future__ import annotations


import httpx

from .sources import GITHUB_API, GITHUB_TIMEOUT, SourceError, _gh_headers


def post_review(owner, repo, number, payload, token, client: httpx.Client | None = None) -> str:
    if not token:
        raise SourceError("--post requires GITHUB_TOKEN (needs pull-request write access)")
    own = client is None
    client = client or httpx.Client(timeout=GITHUB_TIMEOUT)
    try:
        r = client.post(f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{number}/reviews",
                        headers=_gh_headers("application/vnd.github+json", token),
                        json=payload)
        if r.status_code not in (200, 201):
            raise SourceError(f"GitHub rejected the review: HTTP {r.status_code} {r.text[:300]}")
        return r.json().get("html_url", "(posted)")
    except httpx.HTTPError as e:
        raise SourceError(f"GitHub request failed: {e.__class__.__name__}") from None
    finally:
        if own:
            client.close()
