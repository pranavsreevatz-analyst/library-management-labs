from abc import ABC, abstractmethod


class LibraryItem(ABC):
    """Abstract base class representing anything the library can lend out."""

    _id_counter = 1000  # shared across all items so every ID is unique

    def __init__(self, title: str, creator: str, year: int):
        self._item_id = LibraryItem._generate_id()
        self._title = title
        self._creator = creator
        self._year = year
        self._is_available = True

    @classmethod
    def _generate_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter

    # ---- Encapsulated read-only access to internal state ----
    @property
    def item_id(self) -> int:
        return self._item_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def is_available(self) -> bool:
        return self._is_available

    # ---- Controlled state changes (no one can set _is_available directly) ----
    def mark_borrowed(self) -> None:
        self._is_available = False

    def mark_returned(self) -> None:
        self._is_available = True

    # ---- Abstract methods: every subclass MUST provide these ----
    @abstractmethod
    def item_type(self) -> str:
        """Return a human-readable category name, e.g. 'Book'."""
        raise NotImplementedError

    @abstractmethod
    def loan_period_days(self) -> int:
        """Return how many days this type of item can be borrowed for."""
        raise NotImplementedError

    def __str__(self) -> str:
        status = "Available" if self._is_available else "Borrowed"
        return (f"[{self._item_id}] {self.item_type()}: '{self._title}' "
                f"by {self._creator} ({self._year}) - {status}")


class Book(LibraryItem):
    def __init__(self, title: str, author: str, year: int, genre: str, pages: int):
        super().__init__(title, author, year)
        self._genre = genre
        self._pages = pages

    def item_type(self) -> str:
        return "Book"

    def loan_period_days(self) -> int:
        return 14  # books can be kept longest

    def __str__(self) -> str:
        return super().__str__() + f" | Genre: {self._genre}, Pages: {self._pages}"


class Magazine(LibraryItem):
    def __init__(self, title: str, publisher: str, year: int, issue_number: int):
        super().__init__(title, publisher, year)
        self._issue_number = issue_number

    def item_type(self) -> str:
        return "Magazine"

    def loan_period_days(self) -> int:
        return 7

    def __str__(self) -> str:
        return super().__str__() + f" | Issue #{self._issue_number}"


class DVD(LibraryItem):
    def __init__(self, title: str, director: str, year: int, duration_minutes: int):
        super().__init__(title, director, year)
        self._duration = duration_minutes

    def item_type(self) -> str:
        return "DVD"

    def loan_period_days(self) -> int:
        return 5  # shortest loan period

    def __str__(self) -> str:
        return super().__str__() + f" | Duration: {self._duration} min"


class Member:
    """Represents a library member who can borrow items."""

    _id_counter = 100
    MAX_BORROW_LIMIT = 3  # class-level constant shared by all members

    def __init__(self, name: str, email: str):
        self._member_id = Member._generate_id()
        self._name = name
        self._email = email
        self._borrowed_items = []  # encapsulated list of item_ids

    @classmethod
    def _generate_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter

    @property
    def member_id(self) -> int:
        return self._member_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def borrowed_items(self):
        return list(self._borrowed_items)  # return a copy, protect internal list

    def can_borrow(self) -> bool:
        return len(self._borrowed_items) < Member.MAX_BORROW_LIMIT

    def borrow_item(self, item_id: int) -> None:
        self._borrowed_items.append(item_id)

    def return_item(self, item_id: int) -> None:
        self._borrowed_items.remove(item_id)

    def __str__(self) -> str:
        return (f"[{self._member_id}] {self._name} ({self._email}) - "
                f"Borrowed: {len(self._borrowed_items)}/{Member.MAX_BORROW_LIMIT}")
