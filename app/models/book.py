"""
Book Model
==========
Модель книги - центральная сущность каталога
"""

from sqlalchemy import Column, String, Text, Integer, Float, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.database import Base


# Ассоциативная таблица для Many-to-Many связи Book <-> Genre
# Это не модель, а просто таблица для хранения связей
book_genres = Table(
    "book_genres",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
)


class Book(BaseModel):
    """
    Модель книги.

    Связи:
    - Many-to-One с Author (книга принадлежит одному автору)
    - Many-to-One с Publisher (книга издана одним издательством)
    - Many-to-Many с Genre (книга может иметь несколько жанров)

    Attributes:
        title: Название книги
        isbn: ISBN номер (уникальный)
        description: Описание книги
        pages: Количество страниц
        price: Цена
        publication_date: Дата публикации
        language: Язык книги
        author_id: ID автора (Foreign Key)
        publisher_id: ID издательства (Foreign Key)
        author: Автор (relationship)
        publisher: Издательство (relationship)
        genres: Жанры (relationship Many-to-Many)
    """
    __tablename__ = "books"

    title = Column(String(500), nullable=False, index=True)
    isbn = Column(String(20), nullable=True, unique=True, index=True)
    description = Column(Text, nullable=True)
    pages = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    publication_date = Column(Date, nullable=True)
    language = Column(String(50), default="Russian")

    # Foreign Keys
    author_id = Column(
        Integer,
        ForeignKey("authors.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    publisher_id = Column(
        Integer,
        ForeignKey("publishers.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Relationships
    # Many-to-One: Book -> Author
    author = relationship("Author", back_populates="books")

    # Many-to-One: Book -> Publisher
    publisher = relationship("Publisher", back_populates="books")

    # Many-to-Many: Book <-> Genre
    genres = relationship(
        "Genre",
        secondary=book_genres,
        back_populates="books",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title[:30]}...')>"

    @property
    def genre_names(self) -> list[str]:
        """Список названий жанров книги"""
        return [genre.name for genre in self.genres] if self.genres else []

    def add_genre(self, genre):
        """Добавить жанр к книге"""
        if genre not in self.genres:
            self.genres.append(genre)

    def remove_genre(self, genre):
        """Удалить жанр из книги"""
        if genre in self.genres:
            self.genres.remove(genre)

