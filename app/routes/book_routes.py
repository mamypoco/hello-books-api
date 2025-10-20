from flask import Blueprint, make_response, abort
from app.models.book import books

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.get("/")
def get_all_books():
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return books_response

@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)
    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        response = {"message": f"book {book_id} is invalid "}
        abort(make_response(response, 400)) # takes care of python runtime error
    
    for book in books: # books is from module at top
        if book.id == book_id:
            return book
        
    response = {"message": f"book {book_id} is not found"}
    abort(make_response(response, 404))   