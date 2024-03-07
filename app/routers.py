from uuid import uuid4
from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


from .schemas import Book, Review


router = APIRouter(
    prefix="/books",
    tags=["books"],
)

mock_book_db = [
    Book(
        id="8bf1cfb5-799c-44da-bb57-f076c3247024",
        title="Ponniyin Selvan",
        author="Kalki Krishnamurthy",
        publication_year=1954
    ),
    Book(
        id="def18282-4ab2-4504-b90a-637a4d6cc1ce",
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        publication_year=1925
    ),
    Book(
        id="d1cbb3ad-4de3-456a-9d37-a912e098582c",
        title="To Kill a Mockingbird",
        author="Harper Lee",
        publication_year=1960
    ),
    Book(
        id="1e970a18-0c89-4f15-8060-a9a85a6e0cca",
        title="Legend Of Khasak",
        author="O. V. Vijayan",
        publication_year=1969
    ),
    Book(
        id="2db5e921-e748-4b40-a24d-e637860c1dc0",
        title="Randamoozham",
        author="M T Vasudevan Nair",
        publication_year=1984
    ),

]



@router.post("/")
def create_book(book: Book):
    fake_book_db.append(book)
    response_content = {
        "success": True, "message": "Book created successfully", "data": {"book": book}}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_201_CREATED)


@router.get("/")
def show_books():
    response_content = {"success": True,
                        "message": None, "data": fake_book_db}
    return JSONResponse(content=jsonable_encoder(response_content), status_code=status.HTTP_200_OK)
