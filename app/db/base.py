from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL, echo=True)

session_maker = async_sessionmaker(bind=engine)
