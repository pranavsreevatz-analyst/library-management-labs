
class LibraryError(Exception):
    """Base class for all library-related errors."""
    pass


class ItemNotFoundError(LibraryError):
    """Raised when an item ID does not exist in the catalog."""
    pass


class ItemNotAvailableError(LibraryError):
    """Raised when trying to issue an item that is already borrowed."""
    pass


class MemberNotFoundError(LibraryError):
    """Raised when a member ID does not exist in the system."""
    pass


class BorrowLimitExceededError(LibraryError):
    """Raised when a member tries to borrow more items than allowed."""
    pass
