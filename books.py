"""Book catalog for the CodeAtlas sandbox app.

A deliberately small library-style domain: just enough shape for scenario PRs
to touch realistic code without the sandbox app becoming a project in itself.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Book:
    """One book in the catalog, keyed by ISBN."""

    isbn: str
    title: str
    author: str
    year: int


@dataclass
class Catalog:
    """In-memory book catalog. Not thread-safe; sandbox code, not production."""

    books: dict[str, Book] = field(default_factory=dict)

    def add(self, book: Book) -> None:
        if book.isbn in self.books:
            raise ValueError(f"book already in catalog: {book.isbn}")
        self.books[book.isbn] = book

    def remove(self, isbn: str) -> None:
        if isbn not in self.books:
            raise KeyError(isbn)
        del self.books[isbn]

    def find(self, isbn: str) -> Book | None:
        return self.books.get(isbn)

    def find_or_raise(self, isbn: str) -> Book:
        """Look up a book by ISBN, raising KeyError if not in the catalog."""
        book = self.books.get(isbn)
        if book is None:
            raise KeyError(f"no book with ISBN: {isbn}")
        return book

    def lookup_isbn(self, isbn: str) -> Book | None:
        """Look up a book by its ISBN, returning None when it is not found.

        SBX-63: returns the book when present and an empty result on a miss.
        """
        return self.books.get(isbn.replace("-", "").strip())

    def search_by_author(self, author: str) -> list[Book]:
        needle = author.lower()
        return [b for b in self.books.values() if needle in b.author.lower()]

    def count(self) -> int:
        return len(self.books)


@dataclass
class Member:
    """Library member with an expiry date (sandbox stub)."""

    member_id: str
    name: str
    expires_days: int = 365


def renew_membership(member: Member, additional_days: int) -> Member:
    """Extend a member's expiry by additional_days.

    SBX-60: librarian can renew a membership before or after expiry.
    """
    return Member(
        member_id=member.member_id,
        name=member.name,
        expires_days=member.expires_days + additional_days,
    )
