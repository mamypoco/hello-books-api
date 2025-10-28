from flask import Blueprint, make_response, abort, request
from app.models.book import Book
from ..db import db

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.post("")
def create_book():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]

    new_book = Book(title=title, description=description)
    db.session.add(new_book) # tell db to collect change 
    db.session.commit() # tell db to save & commit

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description
    }
    return response, 201 # tuple of 2 values


@books_bp.get("")
def get_all_books():
    query = db.select(Book).order_by(Book.id)
    books = db.session.scalars(query)

    result_list = []

    for book in books:
        result_list.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return result_list

# @books_bp.get("/<book_id>")
# def get_one_book(book_id):
#     book = validate_book(book_id)
#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description
#     }


# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         response = {"message": f"book {book_id} is invalid "}
#         abort(make_response(response, 400)) # takes care of python runtime error
    
#     for book in books: # books is from module at top
#         if book.id == book_id:
#             return book
        
#     response = {"message": f"book {book_id} is not found"}
#     abort(make_response(response, 404))   