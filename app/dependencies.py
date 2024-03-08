from app.db.database import async_session
from app.db.dals import BookDAL, ReviewDAL


async def get_book_dal():
    async with async_session() as session:
        async with session.begin():
            yield BookDAL(session)

async def get_review_dal():
    async with async_session() as session:
        async with session.begin():
            yield ReviewDAL(session)