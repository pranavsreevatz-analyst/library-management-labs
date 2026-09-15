import unittest

from exceptions import InvalidReturnError
from library import Library
from models import Book, Member


class TestReturns(unittest.TestCase):
    def test_wrong_member_cannot_return_item(self):
        library = Library("Return Test")
        book = Book("Dune", "Frank Herbert", 1965, "Sci-Fi", 412)
        alice = Member("Alice", "alice@example.com")
        bob = Member("Bob", "bob@example.com")

        library.add_item(book)
        library.register_member(alice)
        library.register_member(bob)

        transaction = library.issue_item(
            book.item_id, alice.member_id
        )

        with self.assertRaises(InvalidReturnError):
            library.return_item(book.item_id, bob.member_id)

        # The failed operation must not corrupt existing state.
        self.assertFalse(book.is_available)
        self.assertIn(book.item_id, alice.borrowed_items)
        self.assertEqual(bob.borrowed_items, [])
        self.assertIsNone(transaction.return_date)


if __name__ == "__main__":
    unittest.main()