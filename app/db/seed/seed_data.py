from app.schemas import Book, Review

fake_book_data = [
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


fake_review_data = [
    Review(
        id="493ac67b-7a18-4a0f-a1a8-95c71c2a5473",
        book_id="8bf1cfb5-799c-44da-bb57-f076c3247024",
        text="Ponniyin Selvan is a captivating tale! Loved every bit of it.",
        rating=9
    ),
    Review(
        id="2ed3ba04-cd98-4e21-a4c1-17a8c87ba6b5",
        book_id="8bf1cfb5-799c-44da-bb57-f076c3247024",
        text="I didn't enjoy Ponniyin Selvan. Not as good as the movie.",
        rating=3
    ),
    Review(
        id="7df0a5da-d82f-4d22-b81f-6c1fc7a8f9f1",
        book_id="d1cbb3ad-4de3-456a-9d37-a912e098582c",
        text="Beautifully written, highly recommended.",
        rating=10
    ),
    Review(
        id="91c79c85-8b20-4a4d-a083-dc4bd9a183aa",
        book_id="1e970a18-0c89-4f15-8060-a9a85a6e0cca",
        text="Enjoyed reading it, a must-read.",
        rating=7
    ),
    Review(
        id="56c79f23-4aef-4db1-9a50-1f567bd28c94",
        book_id="2db5e921-e748-4b40-a24d-e637860c1dc0",
        text="Intriguing storyline, well-written.",
        rating=9
    ),
]
