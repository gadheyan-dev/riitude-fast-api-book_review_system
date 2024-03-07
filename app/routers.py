from uuid import uuid4
from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse


from .schemas import Book, Review
from .mock_db import mock_book_db, mock_review_db

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.post("/")
def create_book(book: Book):
    mock_book_db.append(book)
    response_content = {
        "success": True, "message": "Book created successfully", "data": {"book": book}}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_201_CREATED)


@router.get("/")
def show_books(author:str = None, publication_year:int=None):
    filtered_books = mock_book_db

    if author:
        filtered_books = [book for book in filtered_books if book.author == author]

    if publication_year:
        filtered_books = [book for book in filtered_books if book.publication_year == publication_year]

    response_content = {"success": True,
                        "message": None, "data": filtered_books}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_200_OK)


@router.post("/{book_id}/reviews/")
def create_review(book_id: uuid4, review:Review):
    if not book_id or not book_id_exists(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    
    mock_review_db.append(review)
    response_content = {
        "success": True, "message": "Review created successfully", "data": {"book_id":book_id, "review": review}}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_201_CREATED)


@router.get("/{book_id}/reviews/")
def show_reviews(book_id: uuid4):
    if not book_id or not book_id_exists(book_id):
        raise HTTPException(status_code=404, detail="The book you provided does not exist.")
    
    filtered_reviews = mock_review_db
    filtered_reviews = [review for review in filtered_reviews if review.book_id == book_id]
    response_content = {"success": True,
                        "message": None, "data": filtered_reviews}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_200_OK)


def book_id_exists(book_id: uuid4):
    for book in mock_book_db:
        if book.id == book_id:
            return True
    return False