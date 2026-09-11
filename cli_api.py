import httpx


BASE_URL = "http://127.0.0.1:8000"


def read_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value > 0:
                return value

            print("Enter a number greater than zero.")

        except ValueError:
            print("Enter a valid whole number.")


def send_request(client, method, path, data=None, params=None):
    try:
        response = client.request(
            method,
            path,
            json=data,
            params=params,
        )

    except httpx.RequestError as error:
        print(f"Could not reach the API: {error}")
        print("Check that the API server is running.")
        return

    if not response.is_success:
        print(f"Request failed — HTTP {response.status_code}")

        try:
            print(response.json())
        except ValueError:
            print(response.text)

        return

    print(f"Success — HTTP {response.status_code}")

    if not response.content:
        return

    result = response.json()

    if isinstance(result, list):
        if not result:
            print("No records found.")

        for record in result:
            print(record)
    else:
        print(result)


def print_menu():
    print("\n===== LIBRARY API CLIENT =====")
    print("1. View items")
    print("2. View members")
    print("3. Borrow an item")
    print("4. Return an item")
    print("5. View transactions")
    print("6. Search items")
    print("7. Add a book")
    print("8. Register a member")
    print("0. Exit")


def main():
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        while True:
            print_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                send_request(client, "GET", "/items")

            elif choice == "2":
                send_request(client, "GET", "/members")

            elif choice == "3":
                data = {
                    "item_id": read_positive_int("Item ID: "),
                    "member_id": read_positive_int("Member ID: "),
                }
                send_request(client, "POST", "/loans", data=data)

            elif choice == "4":
                data = {
                    "item_id": read_positive_int("Item ID: "),
                    "member_id": read_positive_int("Member ID: "),
                }
                send_request(client, "POST", "/returns", data=data)

            elif choice == "5":
                send_request(client, "GET", "/transactions")

            elif choice == "6":
                keyword = input("Title keyword: ")
                send_request(
                    client,
                    "GET",
                    "/items/search",
                    params={"keyword": keyword},
                )

            elif choice == "7":
                data = {
                    "title": input("Title: "),
                    "author": input("Author: "),
                    "year": read_positive_int("Year: "),
                    "genre": input("Genre: "),
                    "pages": read_positive_int("Pages: "),
                }
                send_request(client, "POST", "/books", data=data)

            elif choice == "8":
                data = {
                    "name": input("Member name: "),
                    "email": input("Member email: "),
                }
                send_request(client, "POST", "/members", data=data)

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()