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

    def search_by_author(self, author: str) -> list[Book]:
        needle = author.lower()
        return [b for b in self.books.values() if needle in b.author.lower()]

    def count(self) -> int:
        return len(self.books)
