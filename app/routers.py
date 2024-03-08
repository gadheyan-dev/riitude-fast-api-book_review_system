from uuid import uuid4
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.db.dals import BookDAL, ReviewDAL
from app.dependencies import get_book_dal, get_review_dal
from app.schemas import Book, Review
from app.mock_db import mock_book_db, mock_review_db

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.post("/")
async def create_book(book: Book, book_dal: BookDAL = Depends(get_book_dal)):
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

    await book_dal.create_book(book)
    response_content = {
        "success": True, "message": "Book created successfully", "data": {"book": book}}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_201_CREATED)


@router.get("/")
async def show_books(author: str = None, publication_year: int = None, book_dal: BookDAL = Depends(get_book_dal)):
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
    try:
        books = await book_dal.get_all_books(author, publication_year)
        response_content = {"success": True,
                            "message": None, "data": books}
        return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)

@router.post("/{book_id}/reviews/")
async def create_review(book_id: str, review: Review, book_dal: BookDAL = Depends(get_book_dal), review_dal: ReviewDAL = Depends(get_review_dal)):
    """
    Create a new review for a specific book.

    Args:
        book_id (str): The id of the book in the path parameter.
        review (Review): The review information.

    Returns:
        JSONResponse: JSON response with details about the created review.

    Raises:
        HTTPException: If the book with the given ID is not found or if the provided book_id in the path
        does not match the book_id in the review.
        RequestValidationException: If there is an issue with the request.


    Example Request:
    ```json
    {
      "book_id": "8bf1cfb5-799c-44da-bb57-f076c3247024",
      "review": "Ponniyin Selvan is an okay read. Found some parts interesting, but overall, it didn't fully captivate me.",
      "rating": 6
    },
    ```

    Example Response:
    ```json
    {
        "success": true,
        "message": "Review created successfully",
        "data": {
            
            "review": {
                "id": "4b89456b-4f0d-4d6b-88d5-3ed4e1b5bc8b",
                "book_id": "8bf1cfb5-799c-44da-bb57-f076c3247024",
                "text": "Ponniyin Selvan is an okay read. Found some parts interesting, but overall, it didn't fully captivate me.",
                "rating": 6
            }
        }
    }
    ```
    """
    if not book_id or not book_dal.book_exists(book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id {book_id} not found.")

    if book_id != review.book_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Book id given in path does not match with book id in the review.")

    await review_dal.create_review(review)
    response_content = {
        "success": True, "message": "Review created successfully", "data": {"review": review}}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_201_CREATED)


@router.get("/{book_id}/reviews/")
def show_reviews(book_id: str, book_dal: BookDAL = Depends(get_book_dal), review_dal: ReviewDAL = Depends(get_review_dal)):
    """
    Find and return all the reviews for a given book.

    Args:
        book_id (str): The given id of the book.

    Raises:
        HTTPException: If the provided book_id is empty or does not exist in the database,
                       a 404 NOT FOUND response is raised.

    Returns:
        JSONResponse: A JSON response containing the reviews for the specified book.
                      If successful, returns a 200 OK response with success, message, and data.
                      If not found, returns a 404 NOT FOUND response.
    Example Response:
    ```json
    {
        "success": true,
        "message": null,
        "data": [
            {
                "id": "4b89456b-4f0d-4d6b-88d5-3ed4e1b5bc8b",
                "book_id": "8bf1cfb5-799c-44da-bb57-f076c3247024",
                "text": "Ponniyin Selvan is an okay read. Found some parts interesting, but overall, it didn't fully captivate me.",
                "rating": 6
            }
        ]
    }
    ```
    """
    if not book_id or not book_dal.book_exists(book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The book you provided does not exist.")

    filtered_reviews = mock_review_db
    filtered_reviews = [
        review for review in filtered_reviews if review.book_id == book_id]
    response_content = {"success": True,
                        "message": None, "data": filtered_reviews}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_200_OK)


