import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.book import Book

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    # decorator to create a new database session after request 
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra): 
        db.session.remove()

    with app.app_context():
        # At start of each test, this recreates tables needed for models.
        db.create_all()
        # this suspends. Lines after yield will run after the test
        yield app

    # After test runs, we drop all of the tables, deleting any data created during the test.
    with app.app_context():
        db.drop_all()

# client fixture requests existing app fixture to run first
# this function makes a test client
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_books(app):
    # Arrange
    ocean_book = Book(title="Ocean Book", description="watr 4evr")
    mountain_book = Book(title="Mountain Book",description="i luv 2 climb rocks")

    db.session.add_all([ocean_book, mountain_book])
    # Alternatively, we could do
    # db.session.add(ocean_book)
    # db.session.add(mountain_book)
    db.session.commit()