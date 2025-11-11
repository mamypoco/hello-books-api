from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db


class Genre(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

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