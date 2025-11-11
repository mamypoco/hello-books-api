from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from ..db import db

if TYPE_CHECKING:
    from .book import Book

class Genre(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    books: Mapped[list["Book"]] = relationship(secondary="book_genre", back_populates="genres") 

    def to_dict(self):
        genre_dict = {}
        genre_dict["id"] = self.id
        genre_dict["name"] = self.name

        return genre_dict

    @classmethod
    def from_dict(cls, genre_data):
        new_genre = cls(
            name=genre_data["name"]
        )
        return new_genre