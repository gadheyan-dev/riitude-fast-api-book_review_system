from fastapi import Depends
from typing import List, Optional
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import Book, Review
from app.models import Book as BooksModel, Review as ReviewsModel

class BookDAL():
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_book(self, book:Book):
        db_book = BooksModel(**book.dict())
        self.db.add(db_book)
        await self.db.commit()

    async def get_all_books(self, author:str = None, publication_year:int = None):
        books_query = select(BooksModel)
        if author:
            books_query = books_query.filter(BooksModel.author.ilike(f"%{author}%"))
        if publication_year:
            books_query = books_query.filter(BooksModel.publication_year == publication_year)
        result = await self.db.execute(books_query)
        books = result.scalars().all()
        return books
    
    async def book_exists(self, book_id: str):
        """
        Checks if a given book_id exists in the database.

        Args:
            book_id (str): The unique identifier of the book.

        Returns:
            bool: True if the book_id exists, False otherwise.
        """
        if not book_id:
            return False
        
        books_query = select(BooksModel).filter(BooksModel.id == book_id)
        result = await self.db.execute(books_query)
        if result:
            return True
        return False
    

class ReviewDAL():
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_review(self, review:Review):
        db_review = ReviewsModel(**review.dict())
        self.db.add(db_review)
        await self.db.commit()