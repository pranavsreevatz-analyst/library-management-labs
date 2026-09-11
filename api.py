from threading import Lock

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from exceptions import (
    LibraryError,
    ItemNotFoundError,
    MemberNotFoundError,
)
from library import Library
from main import seed_data
from models import Book, Member


class BookInput(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int = Field(ge=1)
    genre: str = Field(min_length=1)
    pages: int = Field(gt=0)


class MemberInput(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)


class LoanInput(BaseModel):
    item_id: int = Field(gt=0)
    member_id: int = Field(gt=0)


def item_to_dict(item):
    return {
        "item_id": item.item_id,
        "title": item.title,
        "type": item.item_type(),
        "is_available": item.is_available,
        "loan_period_days": item.loan_period_days(),
    }


def transaction_to_dict(txn):
    return {
        "item_id": txn.item_id,
        "member_id": txn.member_id,
        "issue_date": txn.issue_date,
        "due_date": txn.due_date,
        "return_date": txn.return_date,
    }


def create_app():
    app = FastAPI(title="Library Management API")

    library = Library("API Library")
    seed_data(library)
    library_lock = Lock()

    @app.exception_handler(LibraryError)
    async def handle_library_error(request: Request, exc: LibraryError):
        if isinstance(exc, (ItemNotFoundError, MemberNotFoundError)):
            status_code = 404
        else:
            status_code = 409

        return JSONResponse(
            status_code=status_code,
            content={"detail": str(exc)},
        )

    @app.get("/items")
    def list_items():
        with library_lock:
            return [
                item_to_dict(item)
                for item in library.list_all_items()
            ]

    @app.get("/items/search")
    def search_items(keyword: str):
        with library_lock:
            return [
                item_to_dict(item)
                for item in library.search_by_title(keyword)
            ]

    @app.post("/books", status_code=201)
    def add_book(data: BookInput):
        with library_lock:
            book = Book(
                data.title,
                data.author,
                data.year,
                data.genre,
                data.pages,
            )
            library.add_item(book)
            return item_to_dict(book)

    @app.get("/members")
    def list_members():
        with library_lock:
            return [
                {
                    "member_id": member.member_id,
                    "name": member.name,
                    "borrowed_items": member.borrowed_items,
                }
                for member in library.list_members()
            ]

    @app.post("/members", status_code=201)
    def register_member(data: MemberInput):
        with library_lock:
            member = Member(data.name, data.email)
            library.register_member(member)
            return {
                "member_id": member.member_id,
                "name": member.name,
            }

    @app.post("/loans", status_code=201)
    def issue_item(data: LoanInput):
        with library_lock:
            txn = library.issue_item(data.item_id, data.member_id)
            return transaction_to_dict(txn)

    @app.post("/returns")
    def return_item(data: LoanInput):
        with library_lock:
            txn = library.return_item(data.item_id, data.member_id)
            return transaction_to_dict(txn)

    @app.get("/transactions")
    def list_transactions():
        with library_lock:
            return [
                transaction_to_dict(txn)
                for txn in library.list_transactions()
            ]

    return app


app = create_app()