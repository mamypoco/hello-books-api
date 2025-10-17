from flask import Blueprint
from app.models.book import books

# You write this first
books_bp = Blueprint("books_bp", __name__, url_prefix="/")

# Defining endpoint
@books_bp.get("/books")
def get_all_books():
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return books_response