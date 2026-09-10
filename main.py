from library import Library
from models import Book, Magazine, DVD, Member
from exceptions import LibraryError


def seed_data(library: Library):
    """Pre-load a few items/members so the demo isn't empty on first run."""
    library.add_item(Book("Clean Code", "Robert C. Martin", 2008, "Software Engineering", 464))
    library.add_item(Book("The Hobbit", "J.R.R. Tolkien", 1937, "Fantasy", 310))
    library.add_item(Magazine("National Geographic", "NatGeo", 2024, 245))
    library.add_item(DVD("Inception", "Christopher Nolan", 2010, 148))

    library.register_member(Member("Asha Rao", "asha@example.com"))
    library.register_member(Member("Vikram Singh", "vikram@example.com"))


def print_menu():
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. View all items")
    print("2. View available items only")
    print("3. Search items by title")
    print("4. Add a new Book")
    print("5. Add a new Magazine")
    print("6. Add a new DVD")
    print("7. Register a new member")
    print("8. View all members")
    print("9. Issue (borrow) an item")
    print("10. Return an item")
    print("11. View transaction history")
    print("0. Exit")


def read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def main():
    library = Library("City Central Library")
    seed_data(library)

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                items = library.list_all_items()
                print(f"\n-- All Items ({len(items)}) --")
                for item in items:
                    print(item)  # polymorphic __str__ picks the right subclass format

            elif choice == "2":
                items = library.list_available_items()
                print(f"\n-- Available Items ({len(items)}) --")
                for item in items:
                    print(item)

            elif choice == "3":
                keyword = input("Enter title keyword: ")
                results = library.search_by_title(keyword)
                print(f"\n-- Search results for '{keyword}' ({len(results)}) --")
                for item in results:
                    print(item)

            elif choice == "4":
                title = input("Title: ")
                author = input("Author: ")
                year = read_int("Year: ")
                genre = input("Genre: ")
                pages = read_int("Pages: ")
                item_id = library.add_item(Book(title, author, year, genre, pages))
                print(f"Book added with ID {item_id}.")

            elif choice == "5":
                title = input("Title: ")
                publisher = input("Publisher: ")
                year = read_int("Year: ")
                issue = read_int("Issue number: ")
                item_id = library.add_item(Magazine(title, publisher, year, issue))
                print(f"Magazine added with ID {item_id}.")

            elif choice == "6":
                title = input("Title: ")
                director = input("Director: ")
                year = read_int("Year: ")
                duration = read_int("Duration (minutes): ")
                item_id = library.add_item(DVD(title, director, year, duration))
                print(f"DVD added with ID {item_id}.")

            elif choice == "7":
                name = input("Member name: ")
                email = input("Member email: ")
                member_id = library.register_member(Member(name, email))
                print(f"Member registered with ID {member_id}.")

            elif choice == "8":
                members = library.list_members()
                print(f"\n-- Members ({len(members)}) --")
                for m in members:
                    print(m)

            elif choice == "9":
                item_id = read_int("Item ID to issue: ")
                member_id = read_int("Member ID: ")
                txn = library.issue_item(item_id, member_id)
                print(f"Issued! Due date: {txn.due_date}")

            elif choice == "10":
                item_id = read_int("Item ID to return: ")
                member_id = read_int("Member ID: ")
                library.return_item(item_id, member_id)
                print("Item returned. Thank you!")

            elif choice == "11":
                txns = library.list_transactions()
                print(f"\n-- Transactions ({len(txns)}) --")
                for t in txns:
                    print(t)

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid choice, please try again.")

        except LibraryError as e:
            
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
