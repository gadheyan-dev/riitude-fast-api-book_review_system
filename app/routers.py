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
    """
    Create a new book.

    Args:
        book (Book): The book information.

    Returns:
        JSONResponse: JSON response with details about the created book.

    Raises:
        HTTPException: If there is an issue creating the book.
        RequestValidationException: If there is an issue with the request.

    Example Request:
    ```json
    {
        "title": "Francis Ittikkora",
        "author": "T D Ramakrishnan",
        "publication_year": 2009
    }
    ```

    Example Response:
    ```json
    {
        "success": true,
        "message": "Book created successfully",
        "data": {
            "book": {
                "id": "8bf1cfb5-799c-44da-bb57-f076c3247024",
                "title": "Francis Ittikkora",
                "author": "T D Ramakrishnan",
                "publication_year": 2009
            }
        }
    }
    ```
    """
    mock_book_db.append(book)
    response_content = {
        "success": True, "message": "Book created successfully", "data": {"book": book}}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_201_CREATED)


@router.get("/")
def show_books(author: str = None, publication_year: int = None):
    """
    Get a list of books based on optional filters.

    Args:
        author (str, optional): Author name to filter by.
        publication_year (int, optional): Publication year to filter by.

    Returns:
        JSONResponse: JSON response containing the filtered books.

    Example Request:
    ```http
    GET /books/?author=Kalki&publication_year=2022
    ```

    Example Response:
    ```json
    {
        "success": true,
        "message": null,
        "data": [
    {
      "id": "8bf1cfb5-799c-44da-bb57-f076c3247024",
      "title": "Ponniyin Selvan",
      "author": "Kalki Krishnamurthy",
      "publication_year": 1954
    },
    {
      "id": "def18282-4ab2-4504-b90a-637a4d6cc1ce",
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "publication_year": 1925
    },
            // Additional books...
        ]
    }
    ```
    """
    filtered_books = mock_book_db

    if author:
        filtered_books = [
            book for book in filtered_books if author.lower() in book.author.lower()]

    if publication_year:
        filtered_books = [
            book for book in filtered_books if book.publication_year == publication_year]

    response_content = {"success": True,
                        "message": None, "data": filtered_books}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_200_OK)


@router.post("/{book_id}/reviews/")
def create_review(book_id: str, review: Review):
    if not book_id or not book_id_exists(book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id {book_id} not found.")

    if book_id != review.book_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Book id given in path does not match with book id in the review.")

    review.book_id = book_id
    mock_review_db.append(review)
    response_content = {
        "success": True, "message": "Review created successfully", "data": {"book_id": book_id, "review": review}}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_201_CREATED)


@router.get("/{book_id}/reviews/")
def show_reviews(book_id: str):
    if not book_id or not book_id_exists(book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The book you provided does not exist.")

    filtered_reviews = mock_review_db
    print(filtered_reviews)
    filtered_reviews = [
        review for review in filtered_reviews if review.book_id == book_id]
    response_content = {"success": True,
                        "message": None, "data": filtered_reviews}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_200_OK)


def book_id_exists(book_id: uuid4):
    for book in mock_book_db:
        if book.id == book_id:
            return True
    return False
