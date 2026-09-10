from datetime import date, timedelta

from models import LibraryItem, Member
from exceptions import (
    ItemNotFoundError,
    ItemNotAvailableError,
    MemberNotFoundError,
    BorrowLimitExceededError,
)


class Transaction:
    """A simple record of one borrow/return event."""

    def __init__(self, item_id: int, member_id: int, due_date: date):
        self.item_id = item_id
        self.member_id = member_id
        self.issue_date = date.today()
        self.due_date = due_date
        self.return_date = None

    def __str__(self) -> str:
        status = f"Returned on {self.return_date}" if self.return_date else f"Due {self.due_date}"
        return f"Item {self.item_id} <-> Member {self.member_id} | Issued {self.issue_date} | {status}"


class Library:
    def __init__(self, name: str):
        self._name = name
        self._catalog: dict[int, LibraryItem] = {}
        self._members: dict[int, Member] = {}
        self._transactions: list[Transaction] = []

    # ---------------- Catalog / member management ----------------
    def add_item(self, item: LibraryItem) -> int:
        self._catalog[item.item_id] = item
        return item.item_id

    def register_member(self, member: Member) -> int:
        self._members[member.member_id] = member
        return member.member_id

    def _get_item(self, item_id: int) -> LibraryItem:
        item = self._catalog.get(item_id)
        if item is None:
            raise ItemNotFoundError(f"Item ID {item_id} not found in catalog.")
        return item

    def _get_member(self, member_id: int) -> Member:
        member = self._members.get(member_id)
        if member is None:
            raise MemberNotFoundError(f"Member ID {member_id} not found.")
        return member

    # ---------------- Core lending operations ----------------
    def issue_item(self, item_id: int, member_id: int) -> Transaction:
        item = self._get_item(item_id)
        member = self._get_member(member_id)

        if not item.is_available:
            raise ItemNotAvailableError(f"'{item.title}' is already borrowed.")
        if not member.can_borrow():
            raise BorrowLimitExceededError(
                f"{member.name} has reached the borrow limit of {Member.MAX_BORROW_LIMIT}."
            )

        
        due = date.today() + timedelta(days=item.loan_period_days())

        item.mark_borrowed()
        member.borrow_item(item_id)

        txn = Transaction(item_id, member_id, due)
        self._transactions.append(txn)
        return txn

    def return_item(self, item_id: int, member_id: int) -> Transaction:
        item = self._get_item(item_id)
        member = self._get_member(member_id)

        item.mark_returned()
        member.return_item(item_id)

        for txn in reversed(self._transactions):
            if txn.item_id == item_id and txn.member_id == member_id and txn.return_date is None:
                txn.return_date = date.today()
                return txn

        raise LookupError("No open transaction found for this item/member pair.")

    # ---------------- Queries / reporting ----------------
    def list_all_items(self):
        return list(self._catalog.values())

    def list_available_items(self):
        return [item for item in self._catalog.values() if item.is_available]

    def list_members(self):
        return list(self._members.values())

    def list_transactions(self):
        return list(self._transactions)

    def search_by_title(self, keyword: str):
        keyword = keyword.lower()
        return [item for item in self._catalog.values() if keyword in item.title.lower()]
