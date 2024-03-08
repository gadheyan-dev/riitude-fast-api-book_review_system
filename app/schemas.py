from uuid import uuid4
from typing_extensions import Annotated

from pydantic import BaseModel, Field


class Book(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    title: Annotated[str, Field(min_length=3, max_length=200, description="The title of the book.")]
    author: Annotated[str, Field(min_length=2, max_length=100, description="The name of the author")] # Not converting field to separate relation for the sake of simplicity.
    publication_year: Annotated[int, Field(gt=0, description="The year in which the book was published.")]

class Review(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    book_id: Annotated[str, Field(description="The related book id.")]
    text: Annotated[str, Field(min_length=3, max_length=600, description="The review given for the book.")]
    rating: Annotated[int, Field(ge=0, le=10, description="A rating out of 10 given for the book.")]
