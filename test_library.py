

import unittest
from library import Library
from models import Book, Magazine, DVD, Member
from exceptions import (
    ItemNotFoundError,
    ItemNotAvailableError,
    MemberNotFoundError,
    BorrowLimitExceededError,
)


class TestLibraryItems(unittest.TestCase):
    def test_book_type_and_loan_period(self):
        book = Book("1984", "George Orwell", 1949, "Dystopian", 328)
        self.assertEqual(book.item_type(), "Book")
        self.assertEqual(book.loan_period_days(), 14)
        self.assertTrue(book.is_available)

    def test_magazine_loan_period(self):
        mag = Magazine("Time", "Time Inc.", 2024, 10)
        self.assertEqual(mag.item_type(), "Magazine")
        self.assertEqual(mag.loan_period_days(), 7)

    def test_dvd_loan_period(self):
        dvd = DVD("Interstellar", "Christopher Nolan", 2014, 169)
        self.assertEqual(dvd.item_type(), "DVD")
        self.assertEqual(dvd.loan_period_days(), 5)

    def test_polymorphic_behavior(self):
        # Demonstrates polymorphism: same method call, different results
        items = [
            Book("A", "Author", 2020, "Genre", 100),
            Magazine("B", "Pub", 2020, 1),
            DVD("C", "Director", 2020, 90),
        ]
        periods = [item.loan_period_days() for item in items]
        self.assertEqual(periods, [14, 7, 5])

    def test_unique_ids(self):
        b1 = Book("A", "X", 2000, "G", 1)
        b2 = Book("B", "Y", 2001, "G", 1)
        self.assertNotEqual(b1.item_id, b2.item_id)


class TestMember(unittest.TestCase):
    def test_borrow_limit(self):
        member = Member("Test User", "test@example.com")
        for i in range(Member.MAX_BORROW_LIMIT):
            self.assertTrue(member.can_borrow())
            member.borrow_item(i)
        self.assertFalse(member.can_borrow())


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library("Test Library")
        self.book_id = self.library.add_item(Book("Dune", "Frank Herbert", 1965, "Sci-Fi", 412))
        self.member_id = self.library.register_member(Member("Alice", "alice@example.com"))

    def test_issue_and_return(self):
        txn = self.library.issue_item(self.book_id, self.member_id)
        self.assertIsNotNone(txn.due_date)
        item = self.library._get_item(self.book_id)
        self.assertFalse(item.is_available)

        self.library.return_item(self.book_id, self.member_id)
        self.assertTrue(item.is_available)

    def test_issue_unavailable_item_raises(self):
        self.library.issue_item(self.book_id, self.member_id)
        member2 = Member("Bob", "bob@example.com")
        member2_id = self.library.register_member(member2)
        with self.assertRaises(ItemNotAvailableError):
            self.library.issue_item(self.book_id, member2_id)

    def test_issue_nonexistent_item_raises(self):
        with self.assertRaises(ItemNotFoundError):
            self.library.issue_item(99999, self.member_id)

    def test_issue_nonexistent_member_raises(self):
        with self.assertRaises(MemberNotFoundError):
            self.library.issue_item(self.book_id, 99999)

    def test_borrow_limit_exceeded_raises(self):
        # Give the member 3 more items so they hit MAX_BORROW_LIMIT (3)
        ids = [self.library.add_item(Book(f"Book{i}", "Author", 2000, "G", 100)) for i in range(4)]
        for item_id in ids[:3]:
            self.library.issue_item(item_id, self.member_id)
        with self.assertRaises(BorrowLimitExceededError):
            self.library.issue_item(ids[3], self.member_id)

    def test_search_by_title(self):
        results = self.library.search_by_title("dune")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Dune")


if __name__ == "__main__":
    unittest.main()
