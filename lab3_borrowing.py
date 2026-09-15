from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, Lock

from exceptions import ItemNotAvailableError
from library import Library
from models import Book, Member


def main():
    library = Library("Concurrency Lab")

    book = Book("Dune", "Frank Herbert", 1965, "Sci-Fi", 412)
    library.add_item(book)

    members = [
        Member("Alice", "alice@example.com"),
        Member("Bob", "bob@example.com"),
    ]

    for member in members:
        library.register_member(member)

    start_together = Barrier(2)
    borrowing_lock = Lock()

    def attempt_borrow(member):
        start_together.wait()

        try:
            with borrowing_lock:
                library.issue_item(book.item_id, member.member_id)
            return f"{member.name}: borrowed successfully"
        except ItemNotAvailableError:
            return f"{member.name}: item already borrowed"

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(attempt_borrow, members))

    for result in results:
        print(result)

    assert len(library.list_transactions()) == 1
    assert not book.is_available
    assert sum(len(m.borrowed_items) for m in members) == 1

    print("PASS: exactly one member borrowed the item.")


if __name__ == "__main__":
    main()