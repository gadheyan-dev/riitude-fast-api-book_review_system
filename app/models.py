from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    publication_year = Column(Integer, nullable=False)

    reviews = relationship("Review", back_populates="book")


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(String, primary_key=True, index=True, unique=True, nullable=False)
    book_id = Column(String, ForeignKey('books.id'), nullable=False)
    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    book = relationship("Book", back_populates="reviews")
