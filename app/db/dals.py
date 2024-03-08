from fastapi import Depends
from typing import List, Optional
from sqlalchemy import update, delete, or_
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

    async def update_book(self, book_id: str, updated_book_data: Book):
        update_book_query = update(BooksModel).where(BooksModel.id == book_id)
        for field, value in updated_book_data:
            if value:
                update_book_query = update_book_query.values({field:value})
        result = await self.db.execute(update_book_query)
        return result
    
    async def delete_book(self, book_id: str):
        delete_query = delete(BooksModel).where(BooksModel.id == book_id)
        await self.db.execute(delete_query)
        await self.db.commit()
        return None

    async def get_all_books(self, author:str = None, publication_year:int = None):
        books_query = select(BooksModel)
        filters = []
        if author:
            filters.append(BooksModel.author.ilike(f"%{author}%"))
        if publication_year:
            filters.append(BooksModel.publication_year == publication_year)
        
        if filters:
            books_query = books_query.filter(or_(*filters))

        result = await self.db.execute(books_query)
        books = result.scalars().all()
        return books
    
    async def book_exists(self, book_id: str):
        """
        Checks if a given book_id exists in the database and returns the book if it exists. Else False is returned.

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
            return result
        return False
    

class ReviewDAL():
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_review(self, review:Review):
        db_review = ReviewsModel(**review.dict())
        self.db.add(db_review)
        await self.db.commit()

    async def get_reviews(self, book_id:str = None):
        reviews_query = select(ReviewsModel)
        if book_id:
            reviews_query = reviews_query.filter(ReviewsModel.book_id == book_id)
        result = await self.db.execute(reviews_query)
        reviews = result.scalars().all()
        return reviews

    async def update_review(self, review_id: str, updated_review_data: Book):
        update_review_query = update(ReviewsModel).where(ReviewsModel.id == review_id)
        for field, value in updated_review_data:
            if value:
                update_review_query = update_review_query.values({field:value})
        result = await self.db.execute(update_review_query)
        return result

    async def delete_review(self, review_id: str):
        delete_query = delete(ReviewsModel).where(ReviewsModel.id == review_id)
        await self.db.execute(delete_query)
        await self.db.commit()
        return None
    
    async def review_exists(self, review_id: str):
        """
        Checks if a given review_id exists in the database and returns the review if it exists. Else False is returned.

        Args:
            review_id (str): The unique identifier of the review.

        Returns:
            bool: True if the review_id exists, False otherwise.
        """
        if not review_id:
            return False
        
        reviews_query = select(ReviewsModel).filter(ReviewsModel.id == review_id)
        result = await self.db.execute(reviews_query)
        if result:
            return result
        return False