"""Stepwise page state for interactive readers."""

from dataclasses import dataclass, field

from .limits import MIN_PAGE, valid_page_size
from .paginate import page_count, paginate


@dataclass
class PageState:
    """Track the current page of a collection."""

    items: list
    size: int
    page: int = MIN_PAGE
    history: list = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.items, (list, tuple)):
            raise TypeError("items must be a list or tuple")
        self.items = list(self.items)
        self.size = valid_page_size(self.size)
        if isinstance(self.page, bool) or not isinstance(self.page, int):
            raise TypeError("page must be an integer")
        self.page = max(self.page, MIN_PAGE)

    @property
    def count(self):
        """Return the number of pages."""
        return page_count(len(self.items), self.size)

    def current(self):
        """Return the items on the current page."""
        return paginate(self.items, self.page, self.size)

    def next(self):
        """Move to the next page when one exists."""
        limit = max(self.count, MIN_PAGE)
        if self.page < limit:
            self.history.append(self.page)
            self.page += 1
        return self

    def previous(self):
        """Move to the previous page when one exists."""
        if self.page > MIN_PAGE:
            self.history.append(self.page)
            self.page -= 1
        return self

    def at_end(self):
        """Return True when the reader is on the final page."""
        return self.page >= self.count

    def describe(self):
        """Render the current position as text."""
        return f"page {self.page}/{self.count}"
