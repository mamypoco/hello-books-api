from flask import Blueprint, make_response, abort, request, Response
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


@books_bp.get("") # without /, books/ will get 404 though
def get_all_books():
    query = db.select(Book)

    title_param = request.args.get("title") # request.arg object that has title. Don't use ["name"]
    if title_param: 
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    else:
        query = query.order_by(Book.id)

    books = db.session.scalars(query)

    result_list = []

    for book in books:
        result_list.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return result_list

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
    
    except ValueError:
        response = {"message": f"book {book_id} is invalid"}
        abort(make_response(response, 400))
    
    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)

    if not book:
        response = {"message": f"book {book_id} is not found"}
        abort(make_response(response, 404))

    return book


@books_bp.put("/<book_id>")
def update_books(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_book(book_id)
    
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
