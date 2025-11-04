from flask import Blueprint, make_response, abort, request, Response
from app.models.book import Book
from ..db import db
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint("books_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book, request_body)


@bp.get("") # without /, books/ will get 404 though
def get_all_books():
    query = db.select(Book)

    title_param = request.args.get("title") 
    if title_param: 
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    else:
        query = query.order_by(Book.id)

    books = db.session.scalars(query)

    books_response = []

    for book in books:
        books_response.append(book.to_dict())
    return books_response

@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)

    return book.to_dict()
    

@bp.put("/<book_id>")
def update_books(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    
    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
