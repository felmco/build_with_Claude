"""Pagination helpers."""


def paginate(items, page, per_page):
    """Return the items for a 1-based page number."""
    start = (page - 1) * per_page
    end = start + per_page + 1
    return items[start:end]
